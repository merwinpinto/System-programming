#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


// Token structure
typedef struct {
    TokenType type;
    char lexeme[100];
    int lineNumber;
} Token;

// Token types
typedef enum {
    KEYWORD,
    IDENTIFIER,
    CONSTANT,
    SYMBOL,
    END_OF_FILE,
    EMPTY_LINE,
    COMMENT
} TokenType;

// Function to check if a string is a keyword
int isKeyword(char *word) 
{
    char keywords[][10] = {"int", "float", "char", "if", "else", "while", "for", "return", "do"};
    int numKeywords = sizeof(keywords) / sizeof(keywords[0]);

    for (int i = 0; i < numKeywords; ++i) 
    {
        if (strcmp(word, keywords[i]) == 0) 
        {
            return 1;
        }
    }

    return 0;
}

// Function to check if a character is a symbol
int isSymbol(char ch) {
    char symbols[] = "+-*/=(){}[];";
    int numSymbols = sizeof(symbols) / sizeof(symbols[0]);

    for (int i = 0; i < numSymbols; ++i) {
        if (ch == symbols[i]) {
            return 1;
        }
    }

    return 0;
}

// Function to get the next token from the input
Token getNextToken(FILE *fp, int *lineNumber) {
    Token token;
    char ch;

    // Skip whitespaces and handle empty lines
    do {
        ch = fgetc(fp);

        // Check for end of file
        if (ch == EOF) {
            token.type = END_OF_FILE;
            strcpy(token.lexeme, "EOF");
            return token;
        }

        if (ch == '\n') {
            *lineNumber += 1;
            token.type = EMPTY_LINE;
            strcpy(token.lexeme, "Empty Line");
            token.lineNumber = *lineNumber;
            return token;
        }
    } while (isspace(ch));

    // Check for comments
    if (ch == '/') {
        char nextChar = fgetc(fp);
        if (nextChar == '/') {
            *lineNumber += 1;
            token.type = COMMENT;
            strcpy(token.lexeme, "//");
            while ((ch = fgetc(fp)) != '\n' && ch != EOF) {
                strcat(token.lexeme, &ch);
            }
            token.lineNumber = *lineNumber;
            return token;
        } else {
            ungetc(nextChar, fp); // Put back the character
        }
    }

    // Check for symbols
    if (isSymbol(ch)) {
        token.type = SYMBOL;
        token.lexeme[0] = ch;
        token.lexeme[1] = '\0';
        token.lineNumber = *lineNumber;
        return token;
    }

    // Check for keywords or identifiers
    if (isalpha(ch) || ch == '_') {
        int i = 0;
        while (isalnum(ch) || ch == '_') {
            token.lexeme[i++] = ch;
            ch = fgetc(fp);
        }
        token.lexeme[i] = '\0';

        if (isKeyword(token.lexeme)) {
            token.type = KEYWORD;
        } else {
            token.type = IDENTIFIER;
        }

        ungetc(ch, fp); // Put back the last read character
        token.lineNumber = *lineNumber;
        return token;
    }

    // Check for constants (simplified for integers)
    if (isdigit(ch)) {
        int i = 0;
        while (isdigit(ch)) {
            token.lexeme[i++] = ch;
            ch = fgetc(fp);
        }
        token.lexeme[i] = '\0';
        token.type = CONSTANT;

        ungetc(ch, fp); // Put back the last read character
        token.lineNumber = *lineNumber;
        return token;
    }

    // If none of the above, treat it as an error
    token.type = SYMBOL;
    token.lexeme[0] = ch;
    token.lexeme[1] = '\0';
    token.lineNumber = *lineNumber;
    return token;
}

// Function to get the string representation of a TokenType
const char *tokenTypeName(TokenType type) {
    switch (type) {
        case KEYWORD:
            return "KEYWORD";
        case IDENTIFIER:
            return "IDENTIFIER";
        case CONSTANT:
            return "CONSTANT";
        case SYMBOL:
            return "SYMBOL";
        case END_OF_FILE:
            return "END_OF_FILE";
        case EMPTY_LINE:
            return "EMPTY_LINE";
        case COMMENT:
            return "COMMENT";
        default:
            return "UNKNOWN";
    }
}

int main() {
    FILE *fp;
    Token token;
    int lineNumber = 1;

    // Open the input file (replace "input.c" with your input file)
    fp = fopen("input.c", "r");

    if (fp == NULL) {
        perror("Error opening file");
        return 1;
    }

    // Tokenize the input until the end of the file is reached
    do {
        token = getNextToken(fp, &lineNumber);

        // Print the token type name, lexeme, and line number
        printf("Token Type: %s, Lexeme: %s, Line: %d\n", tokenTypeName(token.type), token.lexeme, token.lineNumber);
    } while (token.type != END_OF_FILE);

    // Close the file
    fclose(fp);

    return 0;
}

