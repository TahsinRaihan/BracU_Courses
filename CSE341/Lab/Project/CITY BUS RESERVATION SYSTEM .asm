.MODEL SMALL
.STACK 100H

.DATA
    ; --- BUS DATABASE (ARRAYS) ---
    BusSeatArray   DB 20 DUP(0)    ; 0 = Available, 1 = Occupied
    CategoryArray  DB 20 DUP(0)    ; 1 = Student, 2 = Regular
    FareArchive    DW 20 DUP(0)    ; Stores price paid for refunds
    
    ; --- SESSION DATA ---
    PassengerName  DB 30 DUP('$')  ; Stores current user's name
    
    ; --- FINANCIAL RECORDS ---
    TotalRevenue   DW 0
    TotalTickets   DW 0
    
    ; --- BOOKING TRANSACTION VARS ---
    TicketCount    DW 0            ; Qty selected by user
    TicketPrice    DW 0            ; Price based on category
    CurrentBill    DW 0            ; Total bill for current batch
    LoopCounter    DW 0            ; Safety counter for loops
    
    ; --- SYSTEM CONSTANTS ---
    PRICE_REGULAR  DW 50
    PRICE_STUDENT  DW 30
    ADMIN_PIN      DW 1234         

    ; ---(UI) ---
    MainTitle      DB 10,13,'   =========================================',10,13,'        CITY BUS RESERVATION SYSTEM     ',10,13,'   =========================================$'
    
    LoginMenuStr   DB 10,13,10,13,'   [1] PASSENGER LOGIN',10,13,'   [2] ADMINISTRATOR LOGIN',10,13,'   [3] SHUTDOWN SYSTEM',10,13,10,13,'   >> SELECT OPTION: $'
    
    PassMenuStr    DB 10,13,10,13,'   --- PASSENGER CONTROL PANEL ---',10,13,'   [1] VIEW BUS SEAT MAP',10,13,'   [2] PURCHASE TICKETS ',10,13,'   [3] CANCEL RESERVATION',10,13,'   [4] CHECK SEAT STATUS',10,13,'   [5] LOGOUT',10,13,10,13,'   >> ENTER CHOICE: $'
    
    AdminMenuStr   DB 10,13,10,13,'   --- ADMIN DASHBOARD ---',10,13,'   [1] VIEW FINANCIAL REPORT',10,13,'   [2] VIEW PASSENGER MANIFEST',10,13,'   [3] LOGOUT',10,13,10,13,'   >> ENTER CHOICE: $'

    ; --- SYSTEM PROMPTS ---
    PromptName     DB 10,13,10,13,'   [LOGIN] ENTER YOUR NAME: $'
    PromptQty      DB 10,13,10,13,'   [STEP 1] HOW MANY TICKETS TO BUY? $'
    PromptCat      DB 10,13,'   [STEP 2] SELECT CATEGORY (1=STUDENT / 2=REGULAR): $'
    PromptSeat     DB 10,13,'   [STEP 3] ENTER SEAT NUMBER: $'
    PromptPin      DB 10,13,10,13,'   [SECURITY] ENTER ADMIN ACCESS PIN: $'
    
    PromptBill     DB 10,13,10,13,'   >> TOTAL AMOUNT: $'
    PromptPay      DB ' TAKA | CONFIRM PIN : $'
    
    ; ---NOTIFICATIONS ---
    AlertSuccess   DB 10,13,'   >> SUCCESS: TICKETS CONFIRMED FOR $' 
    AlertRefund    DB 10,13,'   >> SUCCESS: RESERVATION CANCELLED & REFUNDED.$'
    AlertTaken     DB 10,13,'   >> ERROR: SEAT IS OCCUPIED! CHOOSE ANOTHER.$'
    AlertInvalid   DB 10,13,'   >> ERROR: INVALID INPUT!$'
    AlertEmpty     DB 10,13,'   >> ERROR: SEAT IS ALREADY EMPTY.$'
    AlertDenied    DB 10,13,'   >> ERROR: INCORRECT PIN / ACCESS DENIED!$'
    
    ; --- ADMIN REPORTS ---
    RptRevenue     DB 10,13,'   | TOTAL REVENUE GENERATED:  $'
    RptSold        DB 10,13,'   | TOTAL SEATS BOOKED:       $'
    
    InfoBooked     DB 10,13,'   [INFO] STATUS: BOOKED | PASSENGER: $'
    InfoAvail      DB 10,13,'   [INFO] STATUS: AVAILABLE$'
    StrStudent     DB 'STUDENT$'
    StrRegular     DB 'REGULAR$'
    MsgPressKey    DB 10,13,10,13,'   [PRESS ANY KEY TO CONTINUE]$'

    ; --- VISUAL BUS GRAPHICS ---
    BusHeader      DB 10,13,'      ___________________________________',10,13,'     | [DRIVER]                   | EXIT |$'
    BusFooter      DB 10,13,'     |___________________________________|$'
    SpaceGap       DB '   $'
    NewLineChar    DB 10,13,'$'


; MACROS 


ClearScreen MACRO
    MOV AH, 00H
    MOV AL, 03H
    INT 10H
ENDM

DisplayString MACRO STR
    LEA DX, STR
    MOV AH, 9
    INT 21H
ENDM

DisplayChar MACRO C
    MOV DL, C
    MOV AH, 2
    INT 21H
ENDM

; Prints Seat Number 
DisplaySeatNum MACRO
    LOCAL PRT_DOUBLE, END_MACRO
    MOV BX, AX      
    
    CMP BX, 10
    JGE PRT_DOUBLE
    
    DisplayChar '0' ; Print Leading 0
    MOV AX, BX
    ADD AL, 48
    DisplayChar AL
    JMP END_MACRO
    
    PRT_DOUBLE:
    MOV AX, BX
    CALL ShowNumber
    
    END_MACRO:
ENDM

;Multi-digit Number from User
GetInputNumber MACRO
    LOCAL INPUT_L, END_INPUT
    PUSH BX
    PUSH CX
    PUSH DX
    XOR BX, BX
    INPUT_L:
        MOV AH, 1
        INT 21H
        CMP AL, 13
        JE END_INPUT
        SUB AL, 48
        MOV AH, 0
        MOV CX, AX
        MOV AX, BX
        MOV DX, 10
        MUL DX
        ADD AX, CX
        MOV BX, AX
        JMP INPUT_L
    END_INPUT:
        MOV AX, BX
        POP DX
        POP CX
        POP BX
ENDM

;Name String from User
GetInputName MACRO
    LOCAL READ_L, END_READ
    LEA DI, PassengerName
    MOV CX, 0
    READ_L:
        MOV AH, 1
        INT 21H
        CMP AL, 13
        JE END_READ
        MOV [DI], AL
        INC DI
        JMP READ_L
    END_READ:
        MOV BYTE PTR [DI], '$'
ENDM

.CODE

; MAIN PROGRAM ENTRY

MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    
    SystemLoop:
        ClearScreen
        DisplayString MainTitle
        DisplayString LoginMenuStr
        
        MOV AH, 1
        INT 21H
        
        CMP AL, '1'
        JE ModePassenger
        CMP AL, '2'
        JE ModeAdmin
        CMP AL, '3'
        JE Shutdown
        JMP SystemLoop
        
    ModePassenger:
        CALL PassengerSystem
        JMP SystemLoop
        
    ModeAdmin:
        CALL AdminSystem
        JMP SystemLoop
        
    Shutdown:
        MOV AX, 4C00H
        INT 21H
MAIN ENDP


; PROCEDURES (FUNCTIONS)


; --- PASSENGER INTERFACE ---
PassengerSystem PROC
    ClearScreen
    DisplayString MainTitle
    DisplayString PromptName
    GetInputName
    
    PassMenuLoop:
        ClearScreen
        DisplayString MainTitle
        DisplayString NewLineChar
        DisplayString PassengerName
        DisplayString PassMenuStr
        
        MOV AH, 1
        INT 21H
        
        CMP AL, '1'
        JE ActView
        CMP AL, '2'
        JE ActBook
        CMP AL, '3'
        JE ActCancel
        CMP AL, '4'
        JE ActSearch
        CMP AL, '5'
        JE ActLogout
        JMP PassMenuLoop
        
    ActView: 
        CALL ShowSeatMap
        JMP WaitKey
    ActBook: 
        CALL BookTicketSystem ; Feature 3 Logic
        JMP WaitKey
    ActCancel: 
        CALL CancelSystem
        JMP WaitKey
    ActSearch: 
        CALL SearchSystem
        JMP WaitKey
        
    WaitKey:
        DisplayString MsgPressKey
        MOV AH, 7
        INT 21H
        JMP PassMenuLoop
        
    ActLogout:
        RET
PassengerSystem ENDP

; --- ADMIN INTERFACE ---
AdminSystem PROC
    ClearScreen
    DisplayString MainTitle
    DisplayString PromptPin
    GetInputNumber
    
    CMP AX, ADMIN_PIN
    JNE AccessDenied
    
    AdminLoop:
        ClearScreen
        DisplayString MainTitle
        DisplayString AdminMenuStr
        
        MOV AH, 1
        INT 21H
        
        CMP AL, '1'
        JE AdminStats
        CMP AL, '2'
        JE AdminManifest
        CMP AL, '3'
        JE AdminLogout
        JMP AdminLoop
        
    AdminStats:
        ClearScreen
        DisplayString MainTitle
        DisplayString RptRevenue
        MOV AX, TotalRevenue
        CALL ShowNumber
        DisplayString RptSold
        MOV AX, TotalTickets
        CALL ShowNumber
        JMP AdminWait
        
    AdminManifest:
        ClearScreen
        DisplayString MainTitle
        MOV CX, 20
        MOV SI, 0
        ManifestLoop:
            MOV AL, BusSeatArray[SI]
            CMP AL, 1
            JNE NextSeat
            
            DisplayString NewLineChar
            DisplayString SpaceGap
            DisplayChar '['
            MOV AX, SI
            INC AX
            DisplaySeatNum
            DisplayString InfoBooked
            
            MOV AL, CategoryArray[SI]
            CMP AL, 1
            JE ShowStu
            DisplayString StrRegular
            JMP NextSeat
            ShowStu: DisplayString StrStudent
        NextSeat:
            INC SI
            LOOP ManifestLoop
        JMP AdminWait
        
    AdminWait:
        DisplayString MsgPressKey
        MOV AH, 7
        INT 21H
        JMP AdminLoop
        
    AdminLogout: RET
    AccessDenied: 
        DisplayString AlertDenied
        DisplayString MsgPressKey
        MOV AH, 7
        INT 21H
        RET
AdminSystem ENDP

; --- HELPER: PRINT DECIMAL NUMBER ---
ShowNumber PROC
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    MOV CX, 0
    MOV BX, 10
    DigitLoop:
         MOV DX, 0
         DIV BX
         PUSH DX
         INC CX
         CMP AX, 0
         JNE DigitLoop
    PrintLoop:
         POP DX
         ADD DL, 48
         MOV AH, 2
         INT 21H
         LOOP PrintLoop
    POP DX
    POP CX
    POP BX
    POP AX
    RET
ShowNumber ENDP

; --- FEATURE 1: VIEW SEAT MAP ---
ShowSeatMap PROC
    ClearScreen
    DisplayString MainTitle
    DisplayString BusHeader
    MOV CX, 5
    MOV SI, 0
    GridLoop:
        DisplayString NewLineChar
        DisplayString SpaceGap
        CALL DrawSingleSeat
        INC SI
        CALL DrawSingleSeat
        INC SI
        DisplayString SpaceGap
        CALL DrawSingleSeat
        INC SI
        CALL DrawSingleSeat
        INC SI
        LOOP GridLoop
    DisplayString BusFooter
    RET
ShowSeatMap ENDP

DrawSingleSeat PROC
    DisplayChar '['
    MOV AX, SI
    INC AX
    DisplaySeatNum
    DisplayChar ':'
    MOV AL, BusSeatArray[SI]
    CMP AL, 1
    JE DrawBooked
    DisplayChar 'E'
    JMP DrawEnd
    DrawBooked: DisplayChar 'B'
    DrawEnd: DisplayChar ']'
    DisplayChar ' '
    RET
DrawSingleSeat ENDP

; --- FEATURE 3:  BOOKING SYSTEM ---
BookTicketSystem PROC
    ; 1. ASK QUANTITY
    DisplayString PromptQty
    GetInputNumber
    MOV TicketCount, AX
    
    ; 2. ASK CATEGORY 
    AskTypeLoop:
        DisplayString PromptCat
        MOV AH, 1
        INT 21H
        
        CMP AL, '1'
        JE TypeStudent
        CMP AL, '2'
        JE TypeRegular
        JMP AskTypeLoop 
        
    TypeStudent:
        MOV AX, PRICE_STUDENT
        MOV TicketPrice, AX
        JMP CalculateBill
        
    TypeRegular:
        MOV AX, PRICE_REGULAR
        MOV TicketPrice, AX
        
    CalculateBill:
        MOV AX, TicketPrice
        MUL TicketCount
        MOV CurrentBill, AX
        
    ; 3. LOOP SEAT SELECTION
    MOV AX, TicketCount
    MOV LoopCounter, AX
    
    SeatSelectLoop:
        MOV AX, LoopCounter
        CMP AX, 0
        JE VerifyPayment
        
        CALL ShowSeatMap
        DisplayString PromptSeat
        GetInputNumber
        
        ; Validate Range
        CMP AX, 1
        JL ErrorSeat
        CMP AX, 20
        JG ErrorSeat
        DEC AX
        MOV SI, AX
        
        ; Validate Availability
        MOV AL, BusSeatArray[SI]
        CMP AL, 1
        JE ErrorTaken
        
        ; Temporary Booking
        MOV BusSeatArray[SI], 1
        MOV AX, TicketPrice
        MOV FareArchive[SI], AX
        
        MOV AX, TicketPrice
        CMP AX, PRICE_STUDENT
        JNE SetRegType
        MOV CategoryArray[SI], 1
        JMP SaveSession
        SetRegType:
        MOV CategoryArray[SI], 2
        
        SaveSession:
        PUSH SI ; Save Index to Stack for Rollback
        
        DEC LoopCounter
        JMP SeatSelectLoop
        
    ErrorSeat:
        DisplayString AlertInvalid
        MOV AH, 7
        INT 21H
        JMP SeatSelectLoop
    ErrorTaken:
        DisplayString AlertTaken
        MOV AH, 7
        INT 21H
        JMP SeatSelectLoop
        
    VerifyPayment:
        DisplayString PromptBill
        MOV AX, CurrentBill
        CALL ShowNumber
        DisplayString PromptPay
        
        GetInputNumber
        CMP AX, 1234
        JE ProcessPayment
        
        ; ROLLBACK TRANSACTION
        MOV CX, TicketCount
        RollbackLoop:
            POP SI
            MOV BusSeatArray[SI], 0
            MOV FareArchive[SI], 0
            MOV CategoryArray[SI], 0
            LOOP RollbackLoop
        DisplayString AlertDenied
        RET
        
    ProcessPayment:
        ; Commit Transaction (Clear Stack)
        MOV CX, TicketCount
        CommitLoop:
            POP SI
            LOOP CommitLoop
            
        MOV AX, CurrentBill
        ADD TotalRevenue, AX
        MOV AX, TicketCount
        ADD TotalTickets, AX
        
        DisplayString AlertSuccess
        DisplayString PassengerName
        RET
BookTicketSystem ENDP

; --- CANCEL TICKETS ---
CancelSystem PROC
    CALL ShowSeatMap
    DisplayString PromptSeat
    GetInputNumber
    
    CMP AX, 1
    JL CancelErr
    CMP AX, 20
    JG CancelErr
    DEC AX
    MOV SI, AX
    
    MOV AL, BusSeatArray[SI]
    CMP AL, 0
    JE CancelEmpty
    
    MOV AX, FareArchive[SI]
    SUB TotalRevenue, AX
    DEC TotalTickets
    
    MOV BusSeatArray[SI], 0
    MOV FareArchive[SI], 0
    MOV CategoryArray[SI], 0
    
    DisplayString AlertRefund
    RET
    
    CancelEmpty: DisplayString AlertEmpty
                 RET
    CancelErr:   DisplayString AlertInvalid
                 RET
CancelSystem ENDP

; --- SEARCH SEAT ---
SearchSystem PROC
    ClearScreen
    DisplayString PromptSeat
    GetInputNumber
    DEC AX
    MOV SI, AX
    
    MOV AL, BusSeatArray[SI]
    CMP AL, 1
    JE FoundBooked
    DisplayString InfoAvail
    RET
    
    FoundBooked:
    DisplayString InfoBooked
    MOV AL, CategoryArray[SI]
    CMP AL, 1
    JE FoundStu
    DisplayString StrRegular
    RET
    FoundStu: DisplayString StrStudent
    RET
SearchSystem ENDP

END MAIN