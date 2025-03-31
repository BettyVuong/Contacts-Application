//Betty Vuong
//1271673
#ifndef _HELPER_PARSER
#define _HELPER_PARSER

#include <strings.h>
#include <ctype.h>
#include "VCParser.h"

char * propertyWrite(void * prop);
char * dateTimeWrite(void * DT, bool bday);
bool propValidate(void * prop, char * id);
bool paramValidate(void * param);
bool dtValidate(void * prop);
int optionalPropCount(void * obj);
char * bdayToStr(void * obj);
char * anniToStr(void * obj);
char * fnToStr(void * obj);
bool pyToCard(Card ** obj, char * fileName, char * fn);
bool pyEditCard(Card * obj, char * fn, char * fileName);
char * dtToSQL(Card * obj, bool bday);
#endif