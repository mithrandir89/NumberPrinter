/* *****************************************************************************
**
** Author       : Davide Pollarolo
**
** Project      : NURVV Assignment
**
** Description  : Simple program accepting a numerical input, which is then
                  printed in a special format (big-endian and little-endian
                  bytewise).
**
** ************************************************************************** */

/* *****************************************************************************
**    SYSTEM INCLUDE FILES
** ************************************************************************** */
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>

/* *****************************************************************************
**    NON-SYSTEM INCLUDE FILES
** ************************************************************************** */

/* *****************************************************************************
**    ENUM & MACRO DEFINITIONS
** ************************************************************************** */
#define N_BYTES_UINT32      (4) /* Whatever architecture we are speaking of, 1 byte = 8 bits. This means that 32/8 = 4 */
#define EXPECTED_N_ARG      (2) /* Name of the program + number to be printed from user */
#define ARG_NUMBER_INDEX    (1) /* The number will be always in the second slot */

/* *****************************************************************************
**    TYPE DEFINITIONS
** ************************************************************************** */
/* For cleanaliness, define an enum for the endianess type */
typedef enum
{
    LITTLE_ENDIAN   = 0,
    BIG_ENDIAN      = 1,
    
    ENDIANNESS_N   
    
} Endianness_t;

/* Define how to print the bytewise array using flags */
typedef struct
{
    bool BigEndianReverse;
    bool LittleEndianReverse;
    
} ArrayPrintMethod_t;

/* *****************************************************************************
**    LOCAL FUNCTION PROTOTYPES
** ************************************************************************** */
static bool s_ValidateInput(int ArgNumbers, const char* Args[], uint32_t* const ValidatedNumber);
static bool s_ConvertStringToNumber(const char* InputStr, uint64_t* const OutputNum);
static void s_SaveSystemEndiannes( void );
static void s_PrintNumberByteFormat(uint32_t Number);
static void s_PrintByteArray(const uint8_t* const Array, uint8_t ArraySize, bool Reverse);

/* *****************************************************************************
**    LOCAL VARIABLES
** ************************************************************************** */
/* Let's keep it static in the module, as it could be useful in general... */
static Endianness_t SystemEndianness;

/* For each endianness define a LookUpTable with the order of printing */
static const ArrayPrintMethod_t PrintOrderLUT[ENDIANNESS_N] =
{
    {true, false}, /* LITTLE_ENDIAN */
    {false, true}  /* BIG_ENDIAN */
};

/* *****************************************************************************
**    API/PUBLIC FUNCTIONS
** ************************************************************************** */
/* ************************************************************************** */
int main(int argc, char *argv[])
{
    /* C program entry point */
    int Ret;
    uint32_t NumberToPrint;
    
    /* Assume failure */
    Ret = -1;
    
    /* Validate input received */
    if (true == s_ValidateInput(argc, (const char**)argv, &NumberToPrint))
    {
        /* Get system endianess */
        s_SaveSystemEndiannes();
    
        /* Print number */
        s_PrintNumberByteFormat(NumberToPrint);
        
        /* Mark this execution as a success */
        Ret = 0;
    }
    else
    {
        /* Notify error */
        fprintf(stderr, "Error: Invalid input. Expected single positive 32-bit numerical argument in a base-10 format.\n");
    }
    
    return Ret;
}

/* *****************************************************************************
**    LOCAL FUNCTIONS
** ************************************************************************** */
/* ************************************************************************** */
static bool s_ValidateInput(int ArgNumbers,
                            const char* Args[],
                            uint32_t* const ValidatedNumber)
{
    /* Need to reserve space for more than accepted range, as we don't know what to expect in input */
    uint64_t NumberReceived;
    
    /* Assume failure */
    bool Ret = false;
            
    /* Sanity check */
    if(NULL != Args)
    {
        /* First check if we have only one arg as expected */
        if(EXPECTED_N_ARG == ArgNumbers)
        {    
            if (true == s_ConvertStringToNumber(Args[ARG_NUMBER_INDEX], &NumberReceived))
            {                
                /* Validate unsigned 32-bit range */
                if(UINT32_MAX >= NumberReceived)
                {
                    /* Update number only if provided */
                    if (NULL != ValidatedNumber)
                    {
                        *ValidatedNumber = (uint32_t)NumberReceived;
                    }
                                        
                    /* In any case, input is valid */
                    Ret = true;
                }
            }             
        }
    }
    
    return Ret;
}


/* ************************************************************************** */
static bool s_ConvertStringToNumber(const char* InputStr,
                                    uint64_t* const OutputNum)
{
    bool Ret;
    size_t i;
    bool NoDigitFound;
    
    /* Assume failure */
    Ret = false;
    
    if ((NULL != InputStr) && (NULL != OutputNum))
    {
        i = 0;
        NoDigitFound = false;
        
        /* Only numerical values are accepted. This ensures number is interpreted as positive.
        *  As such, iterate over input string and check if they are all digits.
        */
        while('\0' != InputStr[i])
        {
            if(0 == isdigit(InputStr[i]))
            {
                NoDigitFound = true;
                break;
            }
            
            i++;
        }
        
        if (false == NoDigitFound)
        {
            /* Store number (converted) and mark as success */
            *OutputNum = atoll(InputStr);
            Ret = true;
        }
    }
    
    return Ret;
}


/* ************************************************************************** */
static void s_SaveSystemEndiannes( void )
{
    /*  There are architecture that can configure their endianness (such as ARM and PowerPC).
        We can't rely on macros related to the architecture in use this way.
        It is safer and more portable to check endianness at runtime, since there's little cost in it and can be done once at startup.
    */
    
    uint16_t TestNumber;
    uint8_t* NumPtr;
    
    /* 2 bytes are enough to check */
    TestNumber = 0x1;
    NumPtr = (uint8_t*)&TestNumber;
        
    SystemEndianness = ((0x1 == (*NumPtr)) ? LITTLE_ENDIAN : BIG_ENDIAN);
    
    return;
}


/* ************************************************************************** */
static void s_PrintNumberByteFormat(uint32_t Number)
{    
    uint8_t* ArrayPtr;

    /* Save the byteswise array pointer */ 
    ArrayPtr = (uint8_t*)&Number;
    
    /* Use const LookUpTable to choose the order of printing, depending on stored endianness */
    
    /* Print Big Endian first */
    printf("Big Endian: ");
    s_PrintByteArray(ArrayPtr, N_BYTES_UINT32, PrintOrderLUT[SystemEndianness].BigEndianReverse);
    
    /* Print Little endian format as last */
    printf("Little Endian: ");
    s_PrintByteArray(ArrayPtr, N_BYTES_UINT32, PrintOrderLUT[SystemEndianness].LittleEndianReverse);
 
    return;
}

/* ************************************************************************** */
static void s_PrintByteArray(const uint8_t* const Array,
                             uint8_t ArraySize,
                             bool Reverse)
{
    uint8_t i;
    uint8_t CurrByte;
    
    if (NULL != Array)
    {
        for(i = 0; i < ArraySize; i++)
        {
            /* Use pointer arithmetic to find next byte */
            if(true == Reverse)
            {
                CurrByte = *((uint8_t*)(Array + ((ArraySize - 1) - i)));
            }
            else
            {
                CurrByte = *((uint8_t*)(Array + i));
            }
            
            printf("%02X", CurrByte);
            
            /* If last one, do not add space, but a new line */
            if((ArraySize - 1) > i)
            {
                printf(" ");
            }
            else
            {
                printf("\n");
            }
        }
    }

    return;
}
