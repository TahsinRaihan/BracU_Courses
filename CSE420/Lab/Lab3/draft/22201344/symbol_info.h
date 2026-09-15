#include<bits/stdc++.h>
using namespace std;

class symbol_info
{
private:
    string name;
    string type;

    // Write necessary attributes to store what type of symbol it is (variable/array/function)
    string symbol_type;
    // Write necessary attributes to store the type/return type of the symbol (int/float/void/...)
    string data_type;
    string return_type;
    // Write necessary attributes to store the parameters of a function
    int param_count;
    string param_details;
    vector<string> param_type_list;
    // Write necessary attributes to store the array size if the symbol is an array
    int array_size;

public:
    symbol_info(string name, string type)
    {
        this->name = name;
        this->type = type;
        this->symbol_type = "";
        this->data_type = "";
        this->return_type = "";
        this->param_count = 0;
        this->param_details = "";
        this->array_size = 0;
    }
    symbol_info(string name, string type, string data_type)
    {
        this->name = name;
        this->type = type;
        this->symbol_type = "";
        this->data_type = data_type;
        this->return_type = "";
        this->param_count = 0;
        this->param_details = "";
        this->array_size = 0;
    }
    string get_name()
    {
        return name;
    }
    string get_type()
    {
        return type;
    }
    void set_name(string name)
    {
        this->name = name;
    }
    void set_type(string type)
    {
        this->type = type;
    }
    // Write necessary functions to set and get the attributes
    string get_symbol_type()
    {
        return symbol_type;
    }
    void set_symbol_type(string symbol_type)
    {
        this->symbol_type = symbol_type;
    }
    string get_data_type()
    {
        return data_type;
    }
    void set_data_type(string data_type)
    {
        this->data_type = data_type;
    }
    string get_return_type()
    {
        return return_type;
    }
    void set_return_type(string return_type)
    {
        this->return_type = return_type;
    }
    int get_param_count()
    {
        return param_count;
    }
    void set_param_count(int param_count)
    {
        this->param_count = param_count;
    }
    string get_param_details()
    {
        return param_details;
    }
    void set_param_details(string param_details)
    {
        this->param_details = param_details;
    }
    void add_param_type(string type)
    {
        param_type_list.push_back(type);
    }
    vector<string> get_param_type_list()
    {
        return param_type_list;
    }
    int get_array_size()
    {
        return array_size;
    }
    void set_array_size(int array_size)
    {
        this->array_size = array_size;
    }

    ~symbol_info()
    {
        // Write necessary code to deallocate memory, if necessary
    }
};
