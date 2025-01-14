add_executable(parallel main.c)
add_library(cStack concurrentStack.c)
target_link_libraries(parallel io err atomic cStack)
