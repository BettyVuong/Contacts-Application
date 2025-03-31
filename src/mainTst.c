#include "LinkedListAPI.h"
#include "VCParser.h"
#include "VCHelper.h"

int main() {
    Card * test;
    //VCardErrorCode lol = createCard("testCardMin.vcf", &test);
    createCard("bin/cards/testCard-BdayText.vcf", &test);
    // char *tst = cardToString(test);
    // printf("%s\n", tst);
    // free(tst);
    dtToSQL(test, true);
    //char * fix = errorToString(lol);
    //printf("%s", fix);
    // writeCard("test.vcf", test);
    // validateCard(test);
    deleteCard(test);
    //free(test);
    //free(fix);
    return 0;
}