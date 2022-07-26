#include "utils.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

FileReader* new_file_reader(const char* path)
{
    FileReader* self = calloc(1, sizeof(FileReader));
    *self = (FileReader) {
        .fp = fopen(path, "r"),
    };
    assert(self->fp && "could not open file");
    return self;
}

void delete_file_reader(FileReader* self)
{
    fclose(self->fp);
    free(self);
}

size_t file_reader_length(FileReader* self)
{
    fseek(self->fp, 0, SEEK_END);
    return ftell(self->fp);
}

char* file_reader_read(FileReader* self)
{
    size_t length = file_reader_length(self);
    fseek(self->fp, 0, SEEK_SET);
    char* content = calloc(length + 1, sizeof(char));
    fread(content, length, length, self->fp);
    for (int i = 0; i < length; i++)
        if (content[i] == EOF)
            content[i] = '\0';
    return content;
}

char* read_file(const char* path)
{
    FileReader* file = new_file_reader(path);
    char* content = file_reader_read(file);
    delete_file_reader(file);
    return content;
}

FileWriter* new_file_writer(const char* path)
{
    FileWriter* self = calloc(1, sizeof(FileWriter));
    *self = (FileWriter) {
        .fp = fopen(path, "w"),
    };
    assert(self->fp && "could not open file");
    return self;
}

void delete_file_writer(FileWriter* self)
{
    fclose(self->fp);
    free(self);
}

void file_writer_write(FileWriter* self, char* string)
{
    int error = fputs(string, self->fp);
    assert(error != EOF && "could not write to file");
}

void write_file(const char* path, char* string)
{
    FileWriter* writer = new_file_writer(path);
    file_writer_write(writer, string);
    delete_file_writer(writer); 
}
