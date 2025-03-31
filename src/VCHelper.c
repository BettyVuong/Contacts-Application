// Betty Vuong
// Student ID: 1271673
#include "LinkedListAPI.h"
#include "VCParser.h"
#include "VCHelper.h"

char *valueToString(void *toBePrinted)
{
    if (toBePrinted == NULL)
    {
        return NULL;
    }
    // List * temp = (List*) toBePrinted;
    // ListIterator iter = createIterator(temp->values);
    char *str = (char *)toBePrinted;
    char *tmpStr = malloc(sizeof(char) * strlen(str) + 20);
    // strcpy(tmpStr, str);
    sprintf(tmpStr, "%s", str);
    return tmpStr;
}

void deleteValue(void *toBeDeleted)
{
    if (toBeDeleted == NULL)
    {
        return;
    }
    if (toBeDeleted != NULL)
    {
        free(toBeDeleted);
    }
}

int compareValues(const void *first, const void *second)
{
    if (first == NULL || second == NULL)
    {
        return 0; // return false
    }
    char *temp1 = (char *)first;
    char *temp2 = (char *)second;

    return strcmp(temp1, temp2);
}

void deleteParameter(void *toBeDeleted)
{
    if (toBeDeleted == NULL)
    {
        return;
    }
    Parameter *tmp = (Parameter *)toBeDeleted;
    if (tmp->name)
    {
        free(tmp->name);
    }
    if (tmp->value)
    {
        free(tmp->value);
    }
    free(tmp);
}
int compareParameters(const void *first, const void *second)
{
    if (first == NULL || second == NULL)
    {
        return 0; // return false
    }
    Parameter *temp1 = (Parameter *)first;
    Parameter *temp2 = (Parameter *)second;
    // compare
    if (strcmp(temp1->name, temp2->name) == 0 && strcmp(temp1->value, temp2->value) == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
    return 0;
}

char *parameterToString(void *param)
{
    if (param == NULL)
    {
        return NULL;
    }

    Parameter *tmp = (Parameter *)param;
    int len = strlen(tmp->name) + strlen(tmp->value) + 100; // for the space
    char *str = (char *)malloc(sizeof(char) * len + 50);
    sprintf(str, "%s\n%s\n", tmp->name, tmp->value);
    return str;
}
void deleteProperty(void *toBeDeleted)
{
    if (toBeDeleted == NULL)
    {
        return;
    }

    Property *temp = (Property *)toBeDeleted;
    if (temp->name)
    {
        free(temp->name);
    }
    if (temp->group)
    {
        free(temp->group);
    }
    if (temp->parameters != NULL)
    {
        freeList(temp->parameters);
    }
    if (temp->values != NULL)
    {
        freeList(temp->values);
    }
    free(temp);
}
int compareProperties(const void *first, const void *second)
{
    if (first == NULL || second == NULL)
    {
        return 0; // return false
    }
    Property *tmp1 = (Property *)first;
    Property *tmp2 = (Property *)second;
    // compare names
    if (strcmp(tmp1->name, tmp2->name) != 0)
    {
        return 0;
    }

    // compare groups
    if (strcmp(tmp1->group, tmp2->group) != 0)
    {
        return 0;
    }

    // compare values
    List *val1 = tmp1->values;
    List *val2 = tmp2->values;
    ListIterator iter1 = createIterator(val1);
    ListIterator iter2 = createIterator(val2);
    void *elem1;
    void *elem2;
    while ((elem1 = nextElement(&iter1)) != NULL && (elem2 = nextElement(&iter2)) != NULL)
    {
        char *valCmp1 = (char *)elem1;
        char *valCmp2 = (char *)elem2;
        if (strcmp(valCmp1, valCmp2) != 0)
        {
            return 0;
        }
    }

    // compare parameters
    List *par1 = tmp1->parameters;
    List *par2 = tmp2->parameters;
    ListIterator trav1 = createIterator(par1);
    ListIterator trav2 = createIterator(par2);
    while ((elem1 = nextElement(&trav1)) != NULL && (elem2 = nextElement(&trav2)) != NULL)
    {
        char *valCmp1 = (char *)elem1;
        char *valCmp2 = (char *)elem2;
        if (strcmp(valCmp1, valCmp2) != 0)
        {
            return 0;
        }
    }

    return 1;
}

char *propertyToString(void *prop)
{
    if (prop == NULL)
    {
        return NULL;
    }
    Property *temp = (Property *)prop;
    // find the size for each LL
    char *vallist = toString(temp->values);
    char *paramList = toString(temp->parameters);
    int len = strlen(temp->name) + strlen(temp->group) + strlen(paramList) + strlen(vallist) + 100;
    char *str = malloc(sizeof(char) * len);
    sprintf(str, "\nName:%s\nGroup:%s\nParams:%s\nValues:%s", temp->name, temp->group, paramList, vallist);
    free(vallist);
    free(paramList);
    return str;
}
void deleteDate(void *toBeDeleted)
{
    if (toBeDeleted == NULL)
    {
        return;
    }
    if (toBeDeleted != NULL)
    {
        DateTime *temp = (DateTime *)toBeDeleted;
        if (temp->date)
        {
            free(temp->date);
        }
        if (temp->time)
        {
            free(temp->time);
        }
        if (temp->text)
        {
            free(temp->text);
        }
        free(toBeDeleted);
    }
}
int compareDates(const void *first, const void *second)
{
    return 0; // stubbed function for now
}
char *dateToString(void *date)
{
    DateTime *temp = (DateTime *)date;
    // account for the spaces and bool in formatting
    int len = strlen(temp->date) + strlen(temp->time) + strlen(temp->text) + 4;
    char *dateStr = (char *)malloc(sizeof(char) * len);
    // copy to string
    sprintf(dateStr, "%s\n%s\n%s", temp->date, temp->time, temp->text);
    return dateStr;
}

char *propertyWrite(void *prop)
{
    // create a string to parse everything into
    if (prop == NULL)
    {
        // char * temp = malloc(sizeof(char)*4);
        // strcpy(temp, "-1");
        return NULL;
    }
    Property *obj = (Property *)prop;
    if (obj == NULL || obj->name == NULL || obj->group == NULL || obj->parameters == NULL || obj->values == NULL)
    {
        // char * temp = malloc(sizeof(char)*4);
        // strcpy(temp, "-1");
        return NULL;
    }
    // get name
    char *strToFile = malloc(sizeof(char) * strlen(obj->name) + 4);
    sprintf(strToFile, "%s", obj->name);

    // get group if it exists
    int groupLen = strlen(obj->group);
    if (groupLen != 0)
    {                                                // group exists
        int totalLen = groupLen + strlen(strToFile); // get total length of the name + group
        char *strGrpName = malloc(sizeof(char) * totalLen + 4);
        sprintf(strGrpName, "%s.%s", strToFile, obj->group);
        free(strToFile);
        strToFile = malloc(sizeof(char) * strlen(strGrpName) + 4);
        strcpy(strToFile, strGrpName);
        free(strGrpName);
    }

    // now get the parameters
    // get the length to iterate the list
    int paramLLlen = getLength(obj->parameters);
    void *elem;
    char *params;
    int curSize = 1000;
    if (paramLLlen != 0)
    {
        // left here, create an iterator and loop to concat the params
        ListIterator iter = createIterator(obj->parameters);
        params = malloc(curSize);
        sprintf(params, ";");
        while ((elem = nextElement(&iter)) != NULL)
        {
            Parameter *tempParam = (Parameter *)elem;
            char *paramName = tempParam->name;
            char *paramVal = tempParam->value;

            int paramLen = strlen(paramName) + strlen(paramVal);
            char *paramStr = malloc(sizeof(char) * paramLen + 40);

            sprintf(paramStr, "%s=%s;", paramName, paramVal);
            int len = strlen(paramStr) + strlen(params) + 40;
            // not enough space realloc
            if (curSize <= len)
            {
                curSize = len + 1000;
                params = (char *)realloc(params, curSize);
                // params = temp;
            }
            strcat(params, paramStr);
            free(paramStr);
        }
        int lastInd = strlen(params);
        params[lastInd - 1] = ':'; // remove the ';' at the end for a ':'

        // concat to the str
        int totalLen = strlen(strToFile) + strlen(params) + 100;
        strToFile = realloc(strToFile, totalLen);
        strcat(strToFile, params);
        free(params);
    }
    else
    {
        strcat(strToFile, ":");
    }

    // get the values, there's always atleast one so, create the iterator
    ListIterator valTrav = createIterator(obj->values);
    void *trav;
    char *valtoStr = toString(obj->values);
    int valLLLen = (strlen(valtoStr) * 2) + 1000;
    free(valtoStr);
    // realloc the string to create space for the values
    strToFile = realloc(strToFile, valLLLen);
    while ((trav = nextElement(&valTrav)) != NULL)
    {
        char *val = (char *)trav;
        int len = strlen(strToFile) + strlen(val) + 40;
        if (valLLLen <= len)
        {
            valLLLen = len + 1000;
            strToFile = realloc(strToFile, valLLLen);
        }
        strcat(strToFile, val);
        strcat(strToFile, ";");
    }
    int finalLen = strlen(strToFile);
    strToFile[finalLen - 1] = '\0'; // remove the last ";"

    return strToFile;
}

char *dateTimeWrite(void *DT, bool bday)
{
    if (DT == NULL)
    {
        return NULL;
    }
    DateTime *dateProp = (DateTime *)DT;
    if (dateProp == NULL || dateProp->date == NULL || dateProp->time == NULL || dateProp->text == NULL)
    {
        return NULL;
    }
    int len = strlen(dateProp->date) + strlen(dateProp->time) + strlen(dateProp->text) + 200;
    char *str = malloc(sizeof(char) * len);

    // getting the right format
    if (bday == true)
    {
        sprintf(str, "BDAY");
    }
    else
    {
        sprintf(str, "ANNIVERSARY");
    }

    // getting the str
    if (dateProp->isText == true)
    {
        strcat(str, ";VALUE=text:");
        strcat(str, dateProp->text);
    }
    else
    {
        strcat(str, ":");
        char *date = dateProp->date;
        int datelen = strlen(date);

        if (datelen != 0)
        { // there is a date
            strcat(str, date);
        }

        char *time = dateProp->time;
        int timelen = strlen(time);
        if (timelen != 0)
        {
            strcat(str, "T");
            strcat(str, time);
        }
    }

    // adding utc indicator if needed
    if (dateProp->UTC == true)
    {
        strcat(str, "Z");
    }

    return str;
}

bool propValidate(void *prop, char *id)
{
    if (prop == NULL)
    {
        return false;
    }

    Property *validprop = (Property *)prop;
    // validate the specifics, values must have one minimum
    ListIterator iter = createIterator(validprop->values);
    void *elem;
    char *val;
    if ((elem = nextElement(&iter)) != NULL)
    {
        val = (char *)elem;
    }
    // checking if theres the value req
    if (getLength(validprop->values) == 0 && strcmp(val, "") == 0)
    {
        return false;
    }

    if (strcmp(id, "SOURCE") == 0)
    {
    }
    else if (strcmp(id, "KIND") == 0)
    {
    }
    else if (strcmp(id, "XML") == 0)
    {
    }
    else if (strcmp(id, "FN") == 0)
    {
        // N must have a cardinality of 5
        int listLen = getLength(validprop->values);
        if (listLen != 1)
        {
            return false;
        }
    }
    else if (strcmp(id, "N") == 0)
    {
        // N must have a cardinality of 5
        int listLen = getLength(validprop->values);
        if (listLen != 5)
        {
            return false;
        }
    }
    else if (strcmp(id, "NICKNAME") == 0)
    {
    }
    else if (strcmp(id, "PHOTO") == 0)
    {
    }
    else if (strcmp(id, "GENDER") == 0)
    {
        // N must have a cardinality of 1-2
        int listLen = getLength(validprop->values);
        if (listLen < 1 || listLen > 2)
        {
            return false;
        }
    }
    else if (strcmp(id, "ADR") == 0)
    {
        // ADR must have a cardinality of 7
        int listLen = getLength(validprop->values);
        if (listLen != 7)
        {
            return false;
        }
    }
    else if (strcmp(id, "TEL") == 0)
    {
    }
    else if (strcmp(id, "EMAIL") == 0)
    {
    }
    else if (strcmp(id, "IMPP") == 0)
    {
    }
    else if (strcmp(id, "LANG") == 0)
    {
    }
    else if (strcmp(id, "TZ") == 0)
    {
    }
    else if (strcmp(id, "GEO") == 0)
    {
    }
    else if (strcmp(id, "TITLE") == 0)
    {
    }
    else if (strcmp(id, "ROLE") == 0)
    {
    }
    else if (strcmp(id, "LOGO") == 0)
    {
    }
    else if (strcmp(id, "ORG") == 0)
    {
    }
    else if (strcmp(id, "MEMBER") == 0)
    {
    }
    else if (strcmp(id, "RELATED") == 0)
    {
    }
    else if (strcmp(id, "CATEGORIES") == 0)
    {
    }
    else if (strcmp(id, "NOTE") == 0)
    {
    }
    else if (strcmp(id, "PRODID") == 0)
    {
    }
    else if (strcmp(id, "REV") == 0)
    {
    }
    else if (strcmp(id, "SOUND") == 0)
    {
    }
    else if (strcmp(id, "UID") == 0)
    {
    }
    else if (strcmp(id, "CLIENTPIDMAP") == 0)
    {
        // CLIENTPIDMAP must have a cardinality of 2
        int listLen = getLength(validprop->values);
        if (listLen != 2)
        {
            return false;
        }
    }
    else if (strcmp(id, "URL") == 0)
    {
    }
    else if (strcmp(id, "KEY") == 0)
    {
    }
    else if (strcmp(id, "FBURL") == 0)
    {
    }
    else if (strcmp(id, "CALADBURI") == 0)
    {
    }
    else if (strcmp(id, "CALURI") == 0)
    {
    }
    else
    {
        return false;
    }

    // // validate params
    // int len = getLength(validprop->parameters);
    // if (len == 0)
    // {
    //     return false;
    // }
    if(validprop->parameters == NULL){
        return false;
    }
    ListIterator trav = createIterator(validprop->parameters);
    // void *elem;
    while ((elem = nextElement(&trav)) != NULL)
    {
        Parameter *param = (Parameter *)elem;
        bool paramValid = paramValidate(param); // call to check that the parameter is valid
        if (paramValid == false)
        {
            return false;
        }
    }

    return true;
}

bool paramValidate(void *param)
{
    if (param == NULL)
    {
        return false;
    }
    Parameter *temp = (Parameter *)param;

    // check for parameter node
    if (temp->name == NULL || temp->value == NULL || strcmp(temp->name, "") == 0 || strcmp(temp->value, "") == 0)
    {
        return false;
    }

    return true;
}

bool dtValidate(void *prop)
{
    if (prop == NULL)
    {
        return false;
    }
    DateTime *dt = (DateTime *)prop;
    bool utc = dt->UTC;
    bool text = dt->isText;

    // check if the values are filled accordingly
    if (utc == true && text == true)
    {
        return false;
    }

    // text is true but there are values in date time and none for text
    if (text == true && (strlen(dt->date) != 0 || strlen(dt->time) != 0))
    {
        return false;
    }
    else if (text == false && strlen(dt->text) != 0)
    {
        return false;
    }

    // checking for the correct length and digits or -
    // this is only checked when text is false
    if (text == false)
    {
        // check for date
        if (strlen(dt->date) != 0)
        {
            char *date = dt->date;
            if (strlen(date) != 8)
            {
                return false;
            }
            // find if theres anything but - or 1-9
            for (int i = 0; i < strlen(date); i++)
            {
                if (date[i] != '-' && (isdigit(date[i]) == false))
                {
                    return false;
                }
            }
        }

        // check for time
        if (strlen(dt->time) != 0)
        {
            char *time = dt->time;
            if (strlen(time) != 6)
            {
                return false;
            }
            // find if theres anything but - or 1-9
            for (int i = 0; i < strlen(time); i++)
            {
                if (time[i] != '-' && (isdigit(time[i]) == false))
                {
                    return false;
                }
            }
        }
    }

    return true;
}

int optionalPropCount(void *card)
{
    Card *temp = (Card *)card;
    int count = 0;
    // traversing to find the total count of properties
    ListIterator trav = createIterator(temp->optionalProperties);
    void *elem;
    while ((elem = nextElement(&trav)) != NULL)
    {
        count++;
    }

    return count;
}
char *bdayToStr(void *obj)
{
    Card *temp = (Card *)obj;
    DateTime *bday = temp->birthday;
    // assume null
    if (bday == NULL)
    {
        return "";
    }

    // check which attributes to access
    if (bday->isText == true)
    {
        char *text = malloc(sizeof(char) * strlen(bday->text) + 10);
        strcpy(text, bday->text);
        return text;
    }
    else
    {
        char *text = malloc(sizeof(char) * (strlen(bday->date) + strlen(bday->time)) + 80);
        text[0] = '\0';
        if (bday->date != NULL)
        {
            strcat(text, "Date: ");
            strcat(text, bday->date);
            strcat(text, " ");
        }
        if (bday->time != NULL)
        {
            strcat(text, "Time: ");
            strcat(text, bday->time);
        }

        if (bday->date != NULL || bday->time != NULL)
        {
            if (bday->UTC == true)
            {
                strcat(text, " (UTC)");
            }
        }
        return text;
    }
}
char *anniToStr(void *obj)
{
    Card *temp = (Card *)obj;
    DateTime *anni = temp->anniversary;
    // assume null
    if (anni == NULL)
    {
        return "";
    }

    // check which attributes to access
    if (anni->isText == true)
    {
        char *text = malloc(sizeof(char) * strlen(anni->text) + 10);
        strcpy(text, anni->text);
        return text;
    }
    else
    {
        char *text = malloc(sizeof(char) * (strlen(anni->date) + strlen(anni->time)) + 80);
        text[0] = '\0';
        if (anni->date != NULL)
        {
            strcat(text, "Date: ");
            strcat(text, anni->date);
            strcat(text, " ");
        }
        if (anni->time != NULL)
        {
            strcat(text, "Time: ");
            strcat(text, anni->time);
        }

        if (anni->date != NULL || anni->time != NULL)
        {
            if (anni->UTC == true)
            {
                strcat(text, " (UTC)");
            }
        }
        return text;
    }
}
char *fnToStr(void *obj)
{
    Card *temp = (Card *)obj;
    Property *fn = temp->fn;

    if(fn == NULL){
        return "";
    }

    // get the values, there's always atleast one so, create the iterator
    ListIterator valTrav = createIterator(fn->values);
    void *trav;
    char *valtoStr = toString(fn->values);
    int valLLLen = (strlen(valtoStr) * 2) + 100;
    free(valtoStr);
    // realloc the string to create space for the values
    char *strToFile = malloc(sizeof(char) * valLLLen);
    strToFile[0] = '\0';
    while ((trav = nextElement(&valTrav)) != NULL)
    {
        char *val = (char *)trav;
        int len = strlen(strToFile) + strlen(val) + 40;
        if (valLLLen <= len)
        {
            valLLLen = len + 1000;
            strToFile = realloc(strToFile, valLLLen);
        }
        strcat(strToFile, val);
        strcat(strToFile, " ");
    }
    int finalLen = strlen(strToFile);
    strToFile[finalLen - 1] = '\0'; // remove the last ", "

    return strToFile;
}

bool pyToCard(Card **card, char *fileName, char *fn)
{
    *card = malloc(sizeof(Card));
    if (*card == NULL)
    {
        return false;
    }
    // create the card
    //  create the LL
    (*card)->fn = malloc(sizeof(Property));
    (*card)->birthday = NULL;
    (*card)->anniversary = NULL;
    (*card)->fn->parameters = initializeList(&parameterToString, &deleteParameter, &compareParameters);
    (*card)->fn->values = initializeList(&valueToString, &deleteValue, &compareValues);
    (*card)->optionalProperties = initializeList(&propertyToString, &deleteProperty, &compareProperties);

    // loading information into the struct
    (*card)->fn->name = malloc(sizeof(char) * 5);
    strcpy((*card)->fn->name, "FN");
    (*card)->fn->group = malloc(10);
    strcpy((*card)->fn->group, "");
    // create copy of the value, make it safe code
    char *name = malloc(sizeof(char) * strlen(fn) + 50);
    strcpy(name, fn);
    insertBack((*card)->fn->values, name);

    // pass into validate to assure that the struct is properly populated
    VCardErrorCode valid = validateCard((*card));

    if (valid != 0)
    {
        deleteCard((*card));
        return false;
    }

    // write card to file
    VCardErrorCode write = writeCard(fileName, (*card));
    if (write != 0)
    {
        deleteCard((*card));
        return false;
    }
    // otherwise function is successful
    return true;
}

bool pyEditCard(Card *card, char *fn, char *fileName)
{
    // find the fn to update
    //  ListIterator trav = createIterator(card->fn->values);
    //  void * elem;
    //  if((elem = nextElement(&trav)) != NULL){
    //      char * val = (char*) elem;
    //      //char * contact = malloc(sizeof(char)*strlen(val) +10);
    //      //strcpy(contact, val);
    //      //return contact;
    //      val = realloc(val, strlen(fn)+10);
    //      val[0] = '\0';
    //      if(val == NULL){
    //          return false;
    //      }
    //      strcpy(val, fn);
    //  }
    //  Node * tmp = (Node*)trav.current;
    //  if(tmp == NULL){
    //      return false;
    //  } else{
    //      char * cpyFn = malloc(sizeof(char)*strlen(fn)+10);
    //      strcpy(cpyFn, fn);
    //      char * elem = (char *) tmp->data;
    //      free(elem);
    //      //updated
    //      temp->data = cpyFn;
    //  }

    //preliminary validation
    if(card->fn == NULL){
        return false;
    }
    if(card->fn->values == NULL){
        return false;
    }

    // clear the list
    freeList(card->fn->values);
    char *cpyFn = malloc(sizeof(char) * strlen(fn) + 10);
    strcpy(cpyFn, fn);
    // reinit
    card->fn->values = initializeList(&valueToString, &deleteValue, &compareValues);
    insertBack(card->fn->values, cpyFn);

    VCardErrorCode write = writeCard(fileName, card);
    if (write != 0)
    {
        return false;
    }
    return true;
}

char * dtToSQL(Card * obj, bool bday){
    if(obj == NULL){
        return NULL;
    }
    DateTime * dt;
    if(bday == true){
        dt = obj-> birthday;
    } else{
        dt = obj-> anniversary;
    }
    if(dt == NULL){
        return NULL;
    }
    //params check
    if (dt-> isText == true){
        return NULL;
    } else{
        char *text = malloc(sizeof(char) * (strlen(dt->date) + strlen(dt->time)) + 200);
        char *convertDate = malloc(sizeof(char) * (strlen(dt->date) + 100));
        char *convertTime = malloc(sizeof(char) * (strlen(dt->time) + 100));
        strcpy(convertDate, dt->date);
        strcpy(convertTime, dt->time);
        text[0] = '\0';

        //start splitting and recomposing for date
        char year[5], month[3], day[3];
        strncpy(year, convertDate, 4);
        year[4] = '\0';
        strncpy(month, convertDate+4, 2);
        month[2] = '\0';
        strncpy(day,convertDate+6,2);
        day[2] = '\0';
        //build the dt for date
        strcat(text, year);
        strcat(text, "-");
        strcat(text, month);
        strcat(text, "-");
        strcat(text, day);
        strcat(text, " ");

        //for time
        char hour[3], min[3], sec[3];
        strncpy(hour, convertTime, 2);
        hour[2]='\0';
        strncpy(min, convertTime+2, 2);
        min[2] = '\0';
        strncpy(sec, convertTime+4, 2);
        sec[2] = '\0';
        //build the dt for date
        strcat(text, hour);
        strcat(text, ":");
        strcat(text, min);
        strcat(text, ":");
        strcat(text, sec);

        int len = strlen(text);
        text[len] = '\0';
        return text;
    }
}