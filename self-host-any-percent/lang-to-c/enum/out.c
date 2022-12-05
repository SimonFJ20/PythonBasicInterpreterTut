
typedef int i32;

enum MyEnum_id {
    MyEnum_OptionOne,
    MyEnum_OptionTwo,
    MyEnum_OptionThree,
};

struct MyEnum {
    enum MyEnum_id id;
};

enum FatEnum_id {
    FatEnum_OptionOne,
    FatEnum_OptionTwo,
};

struct FatEnum {
    enum FatEnum_id id;
};

struct FatEnum_OptionTwo_params {
    enum FatEnum_id id;
    i32 _0;
    i32 _1;
};

int main() {
    struct MyEnum* choice1 = &(struct MyEnum) {
        .id = MyEnum_OptionOne,
    };
    i32 match_result0;
    switch (choice1->id) {
        case MyEnum_OptionOne:
            match_result0 = 1;
            break;
        case MyEnum_OptionTwo:
            match_result0 = 0;
            break;
        case MyEnum_OptionThree:
            match_result0 = 0;
            break;
    }
    struct FatEnum* choice2 = (struct FatEnum*) &(struct FatEnum_OptionTwo_params) {
        .id = FatEnum_OptionTwo,
        ._0 = 3,
        ._1 = 2,
    };
    i32 a = match_result0;
    i32 match_result1;
    switch (choice2->id) {
        case FatEnum_OptionOne: {
            match_result1 = 0;
            break;
        }
        case FatEnum_OptionTwo: {
            i32 a = ((struct FatEnum_OptionTwo_params*)choice2)->_0;
            i32 b = ((struct FatEnum_OptionTwo_params*)choice2)->_1;
            match_result1 = a + b;
            break;
        }
    }
    i32 b = match_result1;
    return 0;
}
