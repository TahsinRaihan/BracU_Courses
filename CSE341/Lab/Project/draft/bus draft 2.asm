; ============================================
; CITY BUS RESERVATION SYSTEM - EMU8086
; ============================================
; Features:
; 1. Secure Admin Login & Seat Map Visualization
; 2. Ticket Booking & Validation
; 3. Fare Calculation (Student / Regular) + Total Revenue
; 4. Admin Revenue Dashboard
; 5. Ticket Cancellation & Refund
; 6. Search Seat Status (Available / Booked + Category + Fare)
; ============================================

.MODEL SMALL
.STACK 100H

.DATA

; ---------- CONSTANTS ----------
REGULAR_FARE   DW 50       ; regular passenger fare
STUDENT_FARE   DW 30       ; student passenger fare

; ---------- ARRAYS & VARIABLES ----------
seatStatus     DB 20 DUP(0)   ; 0 = empty, 1 = booked
passengerType  DB 20 DUP(0)   ; 0 = none, 1 = student, 2 = regular
farePerSeat    DW 20 DUP(0)   ; fare stored per seat (word)

totalRevenue   DW 0           ; total revenue for the day
currentFare    DW 0           ; temp: last calculated fare

seatsSold      DW 0
studentCount   DW 0
regularCount   DW 0

inputBuffer    DB 6 DUP(0)    ; for reading numbers (max 5 digits + 0)
adminPass      DB '1','2','3','4'  ; admin password = 1234

; ---------- MESSAGES / UI STRINGS ----------
welcomeMsg         DB 13,10,'*** CITY BUS RESERVATION SYSTEM ***',13,10,'$'

mainMenuMsg        DB 13,10,'===== MAIN MENU =====',13,10
                   DB '1. User Panel',13,10
                   DB '2. Admin Panel',13,10
                   DB '3. Exit',13,10
                   DB 'Enter your choice: $'

invalidChoiceMsg   DB 13,10,'Invalid choice. Please try again.$'

userMenuMsg        DB 13,10,'===== USER PANEL =====',13,10
                   DB '1. View Seat Map',13,10
                   DB '2. Book Ticket',13,10
                   DB '3. Cancel Ticket',13,10
                   DB '4. Search Seat',13,10
                   DB '5. Back to Main Menu',13,10
                   DB 'Enter your choice: $'

adminMenuMsg       DB 13,10,'===== ADMIN PANEL =====',13,10
                   DB '1. View Seat Map',13,10
                   DB '2. Revenue Dashboard',13,10
                   DB '3. Search Seat',13,10
                   DB '4. Back to Main Menu',13,10
                   DB 'Enter your choice: $'

adminPassPrompt    DB 13,10,'Enter Admin Password (1234): $'
loginFailMsg       DB 13,10,'Wrong password. Returning to Main Menu.$'

frontTitle         DB 13,10,'          FRONT OF BUS',13,10,'$'
busLine            DB '====================================',13,10,'$'

bookPrompt         DB 13,10,'Enter seat number to book (1-20): $'
passengerTypePrompt DB 13,10,'Passenger Type (1 = Student, 2 = Regular): $'
bookingSuccessMsg  DB 'Ticket booked successfully.',13,10,'$'
seatLabel          DB 'Seat: $'
fareLabel          DB ' Fare: $'
invalidSeatMsg     DB 13,10,'Invalid seat number. Please enter 1-20.$'
seatAlreadyBookedMsg DB 13,10,'This seat is already booked.$'

cancelPrompt       DB 13,10,'Enter seat number to cancel (1-20): $'
cancelSuccessMsg   DB 13,10,'Ticket cancelled and refund processed.$'
seatNotBookedMsg   DB 13,10,'This seat is not currently booked.$'

revenueTitle       DB 13,10,'===== END OF DAY REVENUE SUMMARY =====',13,10,'$'
seatsSoldLabel     DB 'Total seats sold: $'
studentCountLabel  DB 'Student tickets: $'
regularCountLabel  DB 'Regular tickets: $'
totalRevenueLabel  DB 'Total revenue: $'

searchPrompt       DB 13,10,'Enter seat number to search (1-20): $'
seatAvailableMsg   DB 'Status: Available (Empty).',13,10,'$'
seatBookedMsg      DB 'Status: Booked.',13,10,'$'
passengerStudentMsg DB 'Passenger Type: Student.',13,10,'$'
passengerRegularMsg DB 'Passenger Type: Regular.',13,10,'$'
passengerUnknownMsg DB 'Passenger Type: Unknown.',13,10,'$'

.CODE

; ============================================
; NEWLINE: prints CR + LF
; ============================================
NEWLINE PROC
    MOV AH,2
    MOV DL,13       ; CR
    INT 21H
    MOV DL,10       ; LF
    INT 21H
    RET
NEWLINE ENDP

; ============================================
; PRINT_NUM: prints unsigned integer in AX
; ============================================
PRINT_NUM PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX

    CMP AX,0
    JNE PN_NOT_ZERO
    MOV DL,'0'
    MOV AH,2
    INT 21H
    JMP PN_DONE

PN_NOT_ZERO:
    MOV CX,0           ; digit count
PN_DIV_LOOP:
    MOV DX,0
    MOV BX,10
    DIV BX             ; AX = AX / 10, DX = remainder
    PUSH DX            ; save remainder (digit)
    INC CX
    CMP AX,0
    JNE PN_DIV_LOOP

PN_PRINT_LOOP:
    POP DX
    ADD DL,'0'
    MOV AH,2
    INT 21H
    LOOP PN_PRINT_LOOP

PN_DONE:
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PRINT_NUM ENDP

; ============================================
; READ_NUMBER: reads decimal (multi-digit) -> AX
; User types digits then presses ENTER.
; ============================================
READ_NUMBER PROC
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI

    MOV CX,0
    MOV SI,OFFSET inputBuffer

RN_READ_LOOP:
    MOV AH,1
    INT 21H            ; read char into AL (echoed by DOS)
    CMP AL,13          ; ENTER?
    JE RN_CONVERT
    CMP AL,'0'
    JB RN_READ_LOOP
    CMP AL,'9'
    JA RN_READ_LOOP

    MOV [SI],AL
    INC SI
    INC CX
    CMP CX,5           ; max 5 digits
    JL RN_READ_LOOP

RN_CONVERT:
    MOV BYTE PTR [SI],0   ; terminator

    ; convert ASCII digits -> number in AX
    MOV AX,0
    MOV SI,OFFSET inputBuffer

RN_CONV_LOOP:
    MOV DL,[SI]
    CMP DL,0
    JE RN_DONE_CONV

    SUB DL,'0'           ; now DL = digit 0..9

    ; AX = AX * 10 using shift-add (no MUL)
    MOV DX,AX
    SHL AX,1             ; 2*old
    SHL DX,1             ; 2*old
    SHL DX,1             ; 4*old
    SHL DX,1             ; 8*old
    ADD AX,DX            ; 10*old

    ; add digit
    XOR BX,BX
    MOV BL,DL
    ADD AX,BX

    INC SI
    JMP RN_CONV_LOOP

RN_DONE_CONV:
    CALL NEWLINE

RN_DONE:
    POP SI
    POP DX
    POP CX
    POP BX
    RET
READ_NUMBER ENDP

; ============================================
; PrintSeat: prints one seat like [1:E] or [10:B]
; BX = seat index (0..19)
; ============================================
PrintSeat PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI

    ; print '['
    MOV DL,'['
    MOV AH,2
    INT 21H

    ; seat number = BX + 1
    MOV AX,BX
    INC AX
    CALL PRINT_NUM

    MOV DL,':'
    MOV AH,2
    INT 21H

    ; status from seatStatus[BX]
    MOV SI,BX
    MOV AL,seatStatus[SI]
    CMP AL,0
    JE PS_EMPTY
    MOV DL,'B'
    JMP PS_STATUS_DONE
PS_EMPTY:
    MOV DL,'E'
PS_STATUS_DONE:
    MOV AH,2
    INT 21H

    MOV DL,']'
    MOV AH,2
    INT 21H

    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
PrintSeat ENDP

; ============================================
; SHOW SEAT MAP (bus-like layout)
; Seats: 5 rows, 4 seats each (2 left, aisle, 2 right)
; ============================================
ShowSeatMap PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI
    PUSH DI

    CALL NEWLINE
    MOV DX,OFFSET frontTitle
    MOV AH,9
    INT 21H

    MOV DX,OFFSET busLine
    MOV AH,9
    INT 21H

    MOV CX,5          ; 5 rows
    MOV DI,0          ; row index
    MOV SI,0          ; seat index 0..19

RowLoop:
    CALL NEWLINE

    ; print "Row X: "
    MOV DL,'R'
    MOV AH,2
    INT 21H
    MOV DL,'o'
    MOV AH,2
    INT 21H
    MOV DL,'w'
    MOV AH,2
    INT 21H
    MOV DL,' '
    MOV AH,2
    INT 21H

    MOV AX,DI
    INC AX
    CALL PRINT_NUM

    MOV DL,':'
    MOV AH,2
    INT 21H
    MOV DL,' '
    MOV AH,2
    INT 21H

    ; Left two seats (SI and SI+1)
    MOV BX,SI
    CALL PrintSeat
    MOV DL,' '
    MOV AH,2
    INT 21H

    MOV BX,SI
    INC BX
    CALL PrintSeat

    ; aisle gap "   ||   "
    MOV DL,' '
    MOV AH,2
    INT 21H
    MOV DL,' '
    MOV AH,2
    INT 21H
    MOV DL,' '
    MOV AH,2
    INT 21H

    MOV DL,'|'
    MOV AH,2
    INT 21H
    MOV DL,'|'
    MOV AH,2
    INT 21H

    MOV DL,' '
    MOV AH,2
    INT 21H
    MOV DL,' '
    MOV AH,2
    INT 21H
    MOV DL,' '
    MOV AH,2
    INT 21H

    ; Right two seats (SI+2 and SI+3)
    MOV BX,SI
    ADD BX,2
    CALL PrintSeat
    MOV DL,' '
    MOV AH,2
    INT 21H

    MOV BX,SI
    ADD BX,3
    CALL PrintSeat

    ; next row
    ADD SI,4
    INC DI
    LOOP RowLoop

    CALL NEWLINE

    POP DI
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
ShowSeatMap ENDP

; ============================================
; ADMIN LOGIN (Feature 1 secure login)
; returns AL = 1 (success) / 0 (failure)
; ============================================
AdminLogin PROC
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI

    MOV DX,OFFSET adminPassPrompt
    MOV AH,9
    INT 21H

    MOV SI,OFFSET adminPass
    MOV CX,4           ; password length
    MOV BL,0           ; mismatch flag = 0

PW_LOOP:
    MOV AH,1
    INT 21H            ; read char (already echoed)
    CMP AL,[SI]
    JE PW_CHAR_OK
    MOV BL,1           ; mismatch
PW_CHAR_OK:
    INC SI
    LOOP PW_LOOP

    ; flush until ENTER
FlushPW:
    MOV AH,1
    INT 21H
    CMP AL,13
    JNE FlushPW

    CALL NEWLINE

    CMP BL,0
    JNE PW_FAIL
    MOV AL,1
    JMP PW_DONE

PW_FAIL:
    MOV AL,0

PW_DONE:
    POP SI
    POP DX
    POP CX
    POP BX
    RET
AdminLogin ENDP

; ============================================
; BOOK TICKET (Feature 2 + Feature 3)
; ============================================
BookTicket PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI

    CALL NEWLINE
    MOV DX,OFFSET bookPrompt
    MOV AH,9
    INT 21H

    CALL READ_NUMBER      ; AX = seat number

    ; validate 1..20
    CMP AX,1
    JB BT_INVALID
    CMP AX,20
    JA BT_INVALID

    DEC AX
    MOV SI,AX            ; seat index 0..19

    MOV AL,seatStatus[SI]
    CMP AL,0
    JNE BT_ALREADY

    ; ask passenger type
    MOV DX,OFFSET passengerTypePrompt
    MOV AH,9
    INT 21H

    MOV AH,1
    INT 21H              ; read '1' or '2'
    MOV BL,AL
    CALL NEWLINE

    ; determine passenger type
    MOV DL,1             ; default student
    CMP BL,'1'
    JE BT_TYPE_SELECTED
    CMP BL,'2'
    JE BT_TYPE_REG
BT_TYPE_REG:
    MOV DL,2
BT_TYPE_SELECTED:

    ; mark seat booked
    MOV AL,1
    MOV seatStatus[SI],AL
    MOV passengerType[SI],DL

    ; calculate fare (Feature 3)
    CMP DL,1
    JE BT_STUDENT_FARE
    MOV AX,REGULAR_FARE
    JMP BT_FARE_READY
BT_STUDENT_FARE:
    MOV AX,STUDENT_FARE
BT_FARE_READY:
    MOV currentFare,AX

    ; store fare into farePerSeat[SI]
    MOV BX,SI
    SHL BX,1                 ; index * 2
    MOV WORD PTR farePerSeat[BX],AX

    ; update totalRevenue
    MOV DX,totalRevenue
    ADD DX,AX
    MOV totalRevenue,DX

    ; success message
    CALL NEWLINE
    MOV DX,OFFSET bookingSuccessMsg
    MOV AH,9
    INT 21H

    CALL NEWLINE
    MOV DX,OFFSET seatLabel
    MOV AH,9
    INT 21H

    MOV AX,SI
    INC AX
    CALL PRINT_NUM

    MOV DX,OFFSET fareLabel
    MOV AH,9
    INT 21H

    MOV AX,currentFare
    CALL PRINT_NUM
    CALL NEWLINE

    ; show updated seat map right after booking
    CALL ShowSeatMap

    JMP BT_END

BT_INVALID:
    CALL NEWLINE
    MOV DX,OFFSET invalidSeatMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE
    JMP BT_END

BT_ALREADY:
    CALL NEWLINE
    MOV DX,OFFSET seatAlreadyBookedMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE

BT_END:
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
BookTicket ENDP

; ============================================
; CANCEL TICKET (Feature 5)
; ============================================
CancelTicket PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI

    CALL NEWLINE
    MOV DX,OFFSET cancelPrompt
    MOV AH,9
    INT 21H

    CALL READ_NUMBER      ; AX = seat number

    CMP AX,1
    JB CT_INVALID
    CMP AX,20
    JA CT_INVALID

    DEC AX
    MOV SI,AX             ; seat index

    MOV AL,seatStatus[SI]
    CMP AL,1
    JNE CT_NOT_BOOKED

    ; booked -> refund
    MOV BX,SI
    SHL BX,1
    MOV AX,WORD PTR farePerSeat[BX]

    ; update totalRevenue
    MOV DX,totalRevenue
    SUB DX,AX
    MOV totalRevenue,DX

    ; clear data
    MOV BYTE PTR seatStatus[SI],0
    MOV BYTE PTR passengerType[SI],0
    MOV WORD PTR farePerSeat[BX],0

    CALL NEWLINE
    MOV DX,OFFSET cancelSuccessMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE

    ; show updated seat map after cancel
    CALL ShowSeatMap

    JMP CT_END

CT_NOT_BOOKED:
    CALL NEWLINE
    MOV DX,OFFSET seatNotBookedMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE
    JMP CT_END

CT_INVALID:
    CALL NEWLINE
    MOV DX,OFFSET invalidSeatMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE

CT_END:
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
CancelTicket ENDP

; ============================================
; REVENUE DASHBOARD (Feature 4)
; ============================================
RevenueDashboard PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI

    MOV seatsSold,0
    MOV studentCount,0
    MOV regularCount,0

    MOV CX,20
    MOV SI,0

RD_LOOP:
    MOV AL,seatStatus[SI]
    CMP AL,1
    JNE RD_NEXT

    ; seat is booked
    MOV AX,seatsSold
    INC AX
    MOV seatsSold,AX

    MOV AL,passengerType[SI]
    CMP AL,1
    JNE RD_CHECK_REG
    ; student
    MOV AX,studentCount
    INC AX
    MOV studentCount,AX
    JMP RD_NEXT

RD_CHECK_REG:
    CMP AL,2
    JNE RD_NEXT
    ; regular
    MOV AX,regularCount
    INC AX
    MOV regularCount,AX

RD_NEXT:
    INC SI
    LOOP RD_LOOP

    CALL NEWLINE
    MOV DX,OFFSET revenueTitle
    MOV AH,9
    INT 21H
    CALL NEWLINE

    MOV DX,OFFSET seatsSoldLabel
    MOV AH,9
    INT 21H
    MOV AX,seatsSold
    CALL PRINT_NUM
    CALL NEWLINE

    MOV DX,OFFSET studentCountLabel
    MOV AH,9
    INT 21H
    MOV AX,studentCount
    CALL PRINT_NUM
    CALL NEWLINE

    MOV DX,OFFSET regularCountLabel
    MOV AH,9
    INT 21H
    MOV AX,regularCount
    CALL PRINT_NUM
    CALL NEWLINE

    MOV DX,OFFSET totalRevenueLabel
    MOV AH,9
    INT 21H
    MOV AX,totalRevenue
    CALL PRINT_NUM
    CALL NEWLINE

    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
RevenueDashboard ENDP

; ============================================
; SEARCH SEAT (Feature 6)
; ============================================
SearchSeat PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH SI

    CALL NEWLINE
    MOV DX,OFFSET searchPrompt
    MOV AH,9
    INT 21H

    CALL READ_NUMBER       ; AX = seat number

    CMP AX,1
    JB SS_INVALID
    CMP AX,20
    JA SS_INVALID

    DEC AX
    MOV SI,AX

    CALL NEWLINE
    MOV DX,OFFSET seatLabel
    MOV AH,9
    INT 21H

    MOV AX,SI
    INC AX
    CALL PRINT_NUM
    CALL NEWLINE

    ; status
    MOV AL,seatStatus[SI]
    CMP AL,1
    JE SS_BOOKED

    MOV DX,OFFSET seatAvailableMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE
    JMP SS_END

SS_BOOKED:
    MOV DX,OFFSET seatBookedMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE

    ; passenger type
    MOV AL,passengerType[SI]
    CMP AL,1
    JE SS_STUDENT
    CMP AL,2
    JE SS_REGULAR
    JMP SS_UNKNOWN

SS_STUDENT:
    MOV DX,OFFSET passengerStudentMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE
    JMP SS_SHOW_FARE

SS_REGULAR:
    MOV DX,OFFSET passengerRegularMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE
    JMP SS_SHOW_FARE

SS_UNKNOWN:
    MOV DX,OFFSET passengerUnknownMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE

SS_SHOW_FARE:
    MOV BX,SI
    SHL BX,1
    MOV AX,WORD PTR farePerSeat[BX]

    MOV DX,OFFSET fareLabel
    MOV AH,9
    INT 21H
    CALL PRINT_NUM
    CALL NEWLINE
    JMP SS_END

SS_INVALID:
    CALL NEWLINE
    MOV DX,OFFSET invalidSeatMsg
    MOV AH,9
    INT 21H
    CALL NEWLINE

SS_END:
    POP SI
    POP DX
    POP CX
    POP BX
    POP AX
    RET
SearchSeat ENDP

; ============================================
; MAIN
; ============================================
MAIN PROC
    MOV AX,@DATA
    MOV DS,AX

    MOV DX,OFFSET welcomeMsg
    MOV AH,9
    INT 21H

MainMenuLoop:
    CALL NEWLINE
    MOV DX,OFFSET mainMenuMsg
    MOV AH,9
    INT 21H

    MOV AH,1
    INT 21H          ; read choice into AL (echoed once)
    MOV BL,AL
    CALL NEWLINE

    CMP BL,'1'
    JE UserPanel
    CMP BL,'2'
    JE AdminPanel
    CMP BL,'3'
    JE ExitProgram

    MOV DX,OFFSET invalidChoiceMsg
    MOV AH,9
    INT 21H
    JMP MainMenuLoop

; ---------- USER PANEL ----------
UserPanel:
UserMenuLoop:
    CALL NEWLINE
    MOV DX,OFFSET userMenuMsg
    MOV AH,9
    INT 21H

    MOV AH,1
    INT 21H
    MOV BL,AL
    CALL NEWLINE

    CMP BL,'1'
    JE UserViewMap
    CMP BL,'2'
    JE UserBook
    CMP BL,'3'
    JE UserCancel
    CMP BL,'4'
    JE UserSearch
    CMP BL,'5'
    JE MainMenuLoop

    MOV DX,OFFSET invalidChoiceMsg
    MOV AH,9
    INT 21H
    JMP UserMenuLoop

UserViewMap:
    CALL ShowSeatMap
    JMP UserMenuLoop

UserBook:
    CALL BookTicket
    JMP UserMenuLoop

UserCancel:
    CALL CancelTicket
    JMP UserMenuLoop

UserSearch:
    CALL SearchSeat
    JMP UserMenuLoop

; ---------- ADMIN PANEL ----------
AdminPanel:
    CALL AdminLogin
    CMP AL,1
    JE AdminMenu
    ; failed
    MOV DX,OFFSET loginFailMsg
    MOV AH,9
    INT 21H
    JMP MainMenuLoop

AdminMenu:
AdminMenuLoop:
    CALL NEWLINE
    MOV DX,OFFSET adminMenuMsg
    MOV AH,9
    INT 21H

    MOV AH,1
    INT 21H
    MOV BL,AL
    CALL NEWLINE

    CMP BL,'1'
    JE AdminViewMap
    CMP BL,'2'
    JE AdminRevenue
    CMP BL,'3'
    JE AdminSearch
    CMP BL,'4'
    JE MainMenuLoop

    MOV DX,OFFSET invalidChoiceMsg
    MOV AH,9
    INT 21H
    JMP AdminMenuLoop

AdminViewMap:
    CALL ShowSeatMap
    JMP AdminMenuLoop

AdminRevenue:
    CALL RevenueDashboard
    JMP AdminMenuLoop

AdminSearch:
    CALL SearchSeat
    JMP AdminMenuLoop

; ---------- EXIT ----------
ExitProgram:
    MOV AH,4CH
    INT 21H
MAIN ENDP

END MAIN
