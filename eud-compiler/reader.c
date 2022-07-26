#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

FileReader* new_file_reader(FILE* fp)
{
    FileReader* self = calloc(1, sizeof (FileReader));
    *self = (FileReader) {
        .getc = file_reader_getc,
        .delete = delete_file_reader,
        .fp = fp,
    };
    return self;
}

void delete_file_reader(FileReader* self)
{
    free(self);
}

char file_reader_getc(FileReader* self)
{
    return getc(self->fp);
}
