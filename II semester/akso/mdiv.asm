global mdiv


; Argumenty:
;   rdi - wskaźnik do tablicy x
;   rsi - n
;   rdx - y
; Zwraca:
;   rax - reszta z dzielenia

mdiv:
    mov r8, rdx                    ; Przypisuje dzielnik - y do r8.
    xor rdx, rdx                   ; Czyszczę rdx przed dzieleniem.

; Sprawdzenie, czy dzielna jest ujemna.
.check_if_divident_is_negative:
    xor r11, r11                   ; Czyszczę r9 i r11, których używam do
    xor r9, r9                     ; sygnalizowania znaku dzielnej i co obecnie
    cmp qword [rdi + 8 * rsi - 8], 0   ; neguje. Porównuje najbardziej znaczącą
    jns .check_if_divider_is_negative  ; komórkę tablicy z 0. Jeżeli >0 skaczę
                                   ; do sprawdzenia znaku dzielnika.
    inc r9                         ; Zwiększam r9, aby wskazać ujemną dzielną.
    inc r11                        ; Zwiększam r11, aby wskazać, że będę negować
    jmp .change_sign               ; dzielną. Skaczę do pętli zmiany znaku.

; Sprawdzenie, czy dzielnik jest ujemny.
.check_if_divider_is_negative:
    xor r11, r11                   ; Czyszczę r11, bo nie będę już negować dzielnej
    xor r10, r10                   ; Czyszczę r10, używam do sygnalizowania znaku
    test r8, r8                    ; dzielnika. Sprawdzam czy dzielnik jest ujemny.
    jns .divide                    ; Jeżeli r8 > 0 skaczę do pętli dzielenia.
    inc r10                        ; Zwiększam r10, aby wskazać że dzielnik jest
    neg r8                         ; ujemny. Odwracam znak dzielnika.

; Dzielenie elementów tablicy x
.divide:
    mov rcx, rsi                   ; Przenoszę n do rcx.

.divide_loop:
    mov rax, [rdi + 8 * rcx - 8]   ; Przenoszę aktualny element tablicy x do rax.
    div r8                         ; Dzielę rdx:rax przez dzielnik. Iloraz
                                   ; przechowywany jest w rax, reszta w rdx
    mov [rdi + 8 * rcx - 8], rax   ; Przenoszę iloraz z powrotem do tablicy x.
    loop .divide_loop              ; Powtarzam pętlę n razy, aż rcx == 0.

; Normalizacja wyników.
.normalise_results:
    xor r10, r9                    ; Sprawdzam, czy oba r10 i r9 są 0 lub 1.
    jne .change_sign               ; Przechodzę do pętli zmiany znaku, jeśli
                                   ; nie są równe (wynik ujemny).
    cmp qword [rdi + 8 * rsi - 8], 0 ; Porównuje najbardziej znaczącą komórkę
    jns .change_sign_remainder     ; wyniku z 0. Przechodzę do sprawdzenia
    div r10                        ; znaku reszty jeśli >0. W.p.p. wymuszam
                                   ; dzielenie przez 0, by wskazać przepełnienie.
; Wiem, że przepełnienie wystąpi gdy najbardziej znaczący bit ostatniej komórki,
; będzie ustawiony na 1, mimo że wynik powinien być dodatni. Dzielenie przez 0
; wysyła do procesera ten sam sygnał, co powinna funckja mdiv, gdy nastąpi
; przepełnienie.

; Zmiana znaku tablicy x.
.change_sign:
    xor  r10, r10                  ; Czyszczę r10, który używam do indeksowania
    mov rcx, rsi                   ; tablicy x. Przenoszę n do rcx.
    stc                            ; Ustawiam flagę przeniesienia na 1.

.change_sign_loop:
    not qword [rdi + 8 * r10]      ; Neguję komórkę w tablicy x. Dodaję 1 jeśli
    adc qword [rdi + 8 * r10], 0   ; flaga przeniesienia ustawiona jest na 1.
    inc r10                        ; Zwiększam r10, aby przejść do następnego
    loop .change_sign_loop         ; elementu. Powtarzam pętlę aż rcx == 0.
; Używam algorytm negacji liczb w systemie U2 (neguję wszystkie bity i dodaję 1)

    test r11, r11                  ; Sprawdam, czy negujemy dzielną czy wynik.
    jnz .check_if_divider_is_negative ; Jeśli r11 == 1, cofam się, aby sprawdzić
                                   ; czy dzielnik jest ujemny.

; Zmiana znaku reszty.
.change_sign_remainder:
    test r9, r9                    ; Jeśli r9 != 0, to oznacza, że reszta ma
    jz .exit                       ; być ujemna. Przechodzę do wyjścia z funkcji
    neg rdx                        ; jeśli >0. W.p.p. Odwracam znak reszty.

; Wyjście z procedury.
.exit:
    mov rax, rdx                   ; Przenoszę resztę zapisaną w rdx do rax.
    ret                            ; Wychodzę z procedury
