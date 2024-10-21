global _start
global print_crc                    ; funkcja pomocnicza do wypisywania wyniku
 
section .data
first_2_bytes dw 0
last_4_bytes dd 0
buffor_lenght equ 65535
crc_shift: db 64
crc_lenght: db 0
 
section .bss
buffor: resb 65535                  ; maksymalnie mozemy wczytac 2^16 danych
look_up_table: resq 256             ; bo dwa bajty maja maksymalną wartość 65535
output resb 65
 
SYS_OPEN equ 2
SYS_READ equ 0
SYS_WRITE equ 1
STDOUT    equ 1
SYS_CLOSE equ 3
O_RDONLY equ 0
SYS_EXIT equ 60
SEEK_CUR equ 1
SYS_LSEEK equ 8
 
section .text
 
 
_start:
    mov rcx, [rsp]              ; sprawdzam ilość parametrów
    cmp rcx, 3  
    jnz .error
    
    mov rax, [rsp + 24]         ; ładuje drugi paramentr do rax
    xor r10, r10                ; wielomian bede zapisywać w r10
    xor r9, r9                  ; w r9 zapisuje dlugosc wielomianu
 
.load_poly_loop:
    mov dl, [rax + r9]          ; załadowuje bajt z drugiego parametru do dl
    test dl, dl                 ; sprawdzam czy jest zerem
    jz .end_of_load_poly_loop   ; jesli jest zerem to znaczy ze to koniec parametru
    cmp dl, '0'                 ; sprawdzam czy jest zerem czy jedynka w kodzie ASCII
    jz .if_zero
    cmp dl, '1'
    jz .if_one
    jmp .error                  ; w p.p. mamy źle podany parametr
 
.if_one:
    shl r10, 1                  ; przesuwam liczbe w lewo i zwiekszam o jeden 
    inc r10                     ; jesli natrafie na jedynke
    jmp .check_size
 
.if_zero:
    shl r10, 1                  ; przesuwam liczbe w lewo jesli jest zerem                     

.check_size:
    inc r9                      ; sprawdzam czy rozmiar wielomianu nie 
    cmp r9, 64                  ; przekroczył 64
    jg .error
    jmp .load_poly_loop

 
.end_of_load_poly_loop:
    mov [rel crc_lenght], r9     ; zapisuje dlugosc parametru w crc_lenght
    sub [rel crc_shift], r9      ; odejmuje od 64 obecna dlugosc 
    mov cl, byte [rel crc_shift] ; jest to odleglosc o jaka będę przesuwać wynik 
    shl r10, cl                  ; by początek wielomianu był na najbardziej znaczącym
                                 ; bicie rejestru 64 bitowego
                                 ; przesuwam wielomian o wyliczoną odległość
 
    mov rcx, 255                 ; bedę generować look up table dla wszystkich bitów
    lea r8, look_up_table        ; 2^8 = 256, więc ustawiam rcx na 255
                                 ; dla bitu 0 wartość w look_up_table to też 0
.generate_look_up_table:
    mov r9, rcx                  ; przypisuje wartosc obecnego bitu na r9
    shl r9, 56                   ; przesuwam go o 56 w lewo, by początek                         
    mov r11, 8                   ; bajtu byl na najbardziej znaczacej
                                 ; pozycji rejestru 64 bitowego
                                 ; ustawiam r11 na 8, bo bajt ma 8 bitów                         
.generate_loop:
    shl r9, 1                    ; przesuwam, bajt w lewo i sprawdzam flagę
    jnc .end_of_loop             ; carry, mogę go przesuwać w ten sposób
    xor r9, r10                  ; jeśli flaga carry będzie zapalona to znaczy,
                                 ; że muszę xorować resztę bajtu z dzielnikiem
                                 ; wiem, że jedynka która zapaliła flagę carry
                                 ; wyzeruje się z najwyższym wspołczynnikiem wielomianu                  
.end_of_loop:
    dec r11  
    jnz .generate_loop
    mov [r8 + 8 * rcx], r9       ; przypisuje wartosc crc dla danego bitu  
    loop .generate_look_up_table ; do look_up_table
 
 
    mov rax, SYS_OPEN
    mov rdi, [rsp + 16]         ; adres pierwszego argumentu (filename)
    mov rsi, O_RDONLY
    syscall                     ; otwieram plik
    test rax, rax               ; sprawdzam czy operacja się udała
    js .error
 
    ; readind bytes
    mov rdi, rax                ; filedescriptor przenosze do rdi
    xor r10, r10                ; bede miec crc w r10 bo nie potrzebuje juz dzielnika 
 
 ; rdi - filedescriptor
 ; r10 - crc
 ; r8  - adres look_up_table

.reading_loop:              
    mov rax, SYS_READ
    mov rsi, first_2_bytes
    mov rdx, 2
    syscall                    
    cmp rax, 2              ; sprawdzam czy udalo sie odczytac plik
    jne .error_with_unclosed_file
 
    movzx rdx, word [rel first_2_bytes]
 
    mov rax, SYS_READ       ; zaladowuje do bufora ilosc bajtów
    mov rsi, buffor         ; ktore odczytalismy z pierwszych               
    syscall                 ; dwóch bajtów pliku 
    cmp rax, rdx            ; sprawdzam czy operacja się udała
    jnz .error_with_unclosed_file
 
 ; rsi - adres buffora
 ; r10 - akutalny crc
 ; r8  - adres look_up_table
 ; rdx - ilość bajtów w buforze
 
.calculate_crc:        
    mov rcx, rdx            ; wykonuje pętle dla każdego bajta znajdującego
    test rcx, rcx           ; się w buforze. Sprawdzam czy rcx nie jest zerem
    jz .read_last_4_bytes
.crc_loop:
    movzx r9, byte [rsi]    ; przypisuje kolejne bajty do r9
    shl r9, 56              ; przesuwam je w lewo by były na najbardziej znaczącej pozycji 
    xor r9, r10             ; rejestru 64 bitowego, xoruje z poprzednim crc
    shr r9, 56              ; przesuwam w prawo by miały wartosc od 0 - 255, by moc
    shl r10, 8              ; odczytac wartosc z look_up_table, przesuwam crc o 8 w lewo
    xor r10, [r8 + 8 * r9]  ; xoruje poprzednie crc z wartością w look_up_table
    inc rsi
    loop .crc_loop
 
 
 
.read_last_4_bytes:
    mov rax, SYS_READ
    mov rsi, last_4_bytes
    mov rdx, 4
    syscall
    cmp rax, 4                    ; sprawdzam czy udalo sie odczytac plik
    jnz .error_with_unclosed_file
 
    movsxd rsi, dword [rel last_4_bytes]
    mov rax, SYS_LSEEK            ; przesuwam pozycje w obecnie czytanym pliku
    mov rdx, SEEK_CUR             ; o pobrane 4 bajty
    syscall
    test rax, rax                 ; sprawdzam czy się udało
    js .error_with_unclosed_file
 
    test rsi, rsi                 ; sprawdzam czy ostatnie 4 bajty są liczbą ujemną
    jns .reading_loop             ; jeśli są ujemne to neguję je i porównuje z długością 
    neg dword [rel last_4_bytes]  ; obecnie czytanego fragmentu
    movzx edx, word [rel first_2_bytes] 
    add edx, 6
    cmp dword [rel last_4_bytes], edx
    jz .close_file               ; jesli długość się zgadza to kończę wczytywanie danych
    jmp .reading_loop
 
.close_file:
    mov rax, SYS_CLOSE
    syscall
    test rax, rax               ; sprawdzam czy udalo sie zmaknąć plik
    js .error

    mov cl, byte [rel crc_shift]
    shr r10, cl                 ; wyrównuję crc, by miało odpowiednią długość

    movzx r11, byte [rel crc_lenght]
    call print_crc              ; wywołuje funcje wypisującą wynik
    xor rdi, rdi                ; ustawiam kod wyjsci na 0
    jmp .exit

.error_with_unclosed_file:
    mov rax, SYS_CLOSE          ; zamykam plik, po wywołanym błędzie
    syscall
.error:
    mov rdi, 1                  ; ustawiam kod wyjścia na 1
.exit:
    mov rax, SYS_EXIT           ; kończę wykonywanie programu
    syscall 
 
 ; r10 - crc
 ; r11 - dlugość jaką będzie miał crc zapisany binarnie

print_crc:                  ; funkcja wypisujaca wynik
    mov rsi, output + 64
    mov byte [rsi], 10      ; oznaczam koniec linii na ostatnim bicie
    mov rcx, r11            ; wypisywanego napisu
 
.print_loop:
    dec rsi 
    mov byte [rsi], '0'     ; zapisuje pod danym adresem 0 w kodzie ASCII
    shr r10, 1              ; przesuwam liczbe w prawo jesli flaga carry
    jnc .add_zero           ; bedzie zapalona to zwiększam ją o 1 by 
    inc byte [rsi]          ; uzyskać 1 w kodzie ASCII
.add_zero:
    loop .print_loop
 
    mov rdx, r11
    inc rdx                 ; zwiekszam o jeden by wypisal znak zakonczenia linii
    mov rax, SYS_WRITE
    mov rdi, STDOUT
    syscall 
    ret
 