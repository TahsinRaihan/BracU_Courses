.MODEL SMALL
.STACK 100H
.DATA
    MSG1    DB 10,13,"ENTER A HEX DIGIT: $" 
    MSG2    DB 10,13,"IN DECIMAL IT IS: $"
    MSG3    DB 10,13,"DO YOU WANT TO DO IT AGAIN? (Y/N): $"
    MSG_ERR DB 10,13,"ILLEGAL CHARACTER - TRY AGAIN.$"

.CODE
MAIN PROC
    ; Initialize Data Segment
    MOV AX, @DATA
    MOV DS, AX

START:

    LEA DX, MSG1
    MOV AH, 9
    INT 21H


    MOV AH, 1
    INT 21H
    MOV BL, AL      ; Save input in BL for later

    ; 3. Validation Logic
    ; Check if input is '0' to '9'
    CMP BL, '0'
    JB  CHECK_HEX   ; If below '0', check if it's a letter (or illegal)
    CMP BL, '9'
    JBE IS_DIGIT    ; If '0'-'9', it is a digit

CHECK_HEX:
    ; Check if input is 'A' to 'F'
    CMP BL, 'A'
    JB  ILLEGAL     ; If below 'A' (and wasn't a digit), it's illegal
    CMP BL, 'F'
    JBE IS_HEX      ; If 'A'-'F', it is valid hex
    
    ; If we get here, it's above 'F', so illegal
    JMP ILLEGAL

ILLEGAL:
    ; Print Error Message and restart
    LEA DX, MSG_ERR
    MOV AH, 9
    INT 21H
    JMP START

; --- PRINTING LOGIC ---

IS_DIGIT:
    ; Case: 0-9
    ; Display Result Message
    LEA DX, MSG2
    MOV AH, 9
    INT 21H

    ; Print the digit exactly as entered
    MOV DL, BL
    MOV AH, 2
    INT 21H
    JMP ASK_AGAIN

IS_HEX:
    ; Case: A-F (Needs to print 10, 11, 12...)
    ; Display Result Message
    LEA DX, MSG2
    MOV AH, 9
    INT 21H

    ; Step 1: Print the '1' (for the tens place)
    MOV DL, '1'
    MOV AH, 2
    INT 21H

    ; Step 2: Calculate the second digit
    ; 'A' (65) -> needs to be '0' (48). 65 - 17 = 48
    ; 'B' (66) -> needs to be '1' (49).
    MOV DL, BL
    SUB DL, 17      ; Convert A-F to 0-5
    MOV AH, 2
    INT 21H
    JMP ASK_AGAIN

; --- REPEAT LOGIC ---

ASK_AGAIN:
    LEA DX, MSG3
    MOV AH, 9
    INT 21H

    MOV AH, 1
    INT 21H

    ; Check for 'y'
    CMP AL, 'y'
    JE  START
    
    ; Check for 'Y'
    CMP AL, 'Y'
    JE  START

    ; If anything else, fall through to exit

EXIT:
    MOV AX, 4C00H
    INT 21H
MAIN ENDP
END MAIN