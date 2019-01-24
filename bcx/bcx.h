/// @file
/// @brief embedded runtime (portable core) headers

/// @defgroup bcx embedded runtime (portable part)
/// @{

#ifndef _H_BCX
#define _H_BCX

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

/// @defgroup vm Virtual Machine
/// @{
						/// @brief bytecode interpreter
extern void VM(void);
						/// @brief current command opcode
extern uint8_t op;

/// @defgroup config Configuration
/// @{

#define CELL uint16_t

#define Msz	0x1000
#define Rsz 0x100
#define Dsz 0x10

/// @}

						/// @brief main memory
extern CELL M[Msz];
						/// @brief instruction pointer
extern CELL Ip;
						/// @brief compiler pointer
extern CELL Cp;

/// @defgroup op Command opcodes
/// @{

						/// @ref NOP
#define op_NOP	0x00
						/// @ref BYE
#define op_BYE	0xFF

/// @}

/// @defgroup code Core commands
/// @{

/// `NOP ( -- )` do nothing
extern void NOP(void);

/// `BYE ( -- )` stop user session
extern void BYE(void);

/// @}

/// @defgroup debug Debug interface
/// @{

/// `DUMP ( -- )` dump main memory
extern void DUMP(void);

/// trace flag: print execution log
extern bool trace;

/// @}

/// @}

/// @}

#endif // _H_BCX
