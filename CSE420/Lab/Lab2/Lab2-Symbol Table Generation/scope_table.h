#include "symbol_info.h"

class scope_table
{
private:
    int bucket_count;
    int unique_id;
    scope_table *parent_scope = NULL;
    vector<list<symbol_info *>> table;

    int hash_function(string name)
    {
        // write your hash function here
        int sum = 0;
        for (int i = 0; i < name.length(); i++)
        {
            sum = sum + (int)name[i];
        }
        return sum % bucket_count;
    }

public:
    scope_table();
    scope_table(int bucket_count, int unique_id, scope_table *parent_scope);
    scope_table *get_parent_scope();
    int get_unique_id();
    symbol_info *lookup_in_scope(symbol_info* symbol);
    bool insert_in_scope(symbol_info* symbol);
    bool delete_from_scope(symbol_info* symbol);
    void print_scope_table(ofstream& outlog);
    ~scope_table();

    // you can add more methods if you need
};

// complete the methods of scope_table class
scope_table::scope_table()
{
    bucket_count = 0;
    unique_id = 0;
    parent_scope = NULL;
}

scope_table::scope_table(int bucket_count, int unique_id, scope_table *parent_scope)
{
    this->bucket_count = bucket_count;
    this->unique_id = unique_id;
    this->parent_scope = parent_scope;
    table.resize(bucket_count);
}

scope_table *scope_table::get_parent_scope()
{
    return parent_scope;
}

int scope_table::get_unique_id()
{
    return unique_id;
}

symbol_info *scope_table::lookup_in_scope(symbol_info* symbol)
{
    int index = hash_function(symbol->get_name());
    for (list<symbol_info *>::iterator it = table[index].begin(); it != table[index].end(); it++)
    {
        if ((*it)->get_name() == symbol->get_name())
        {
            return *it;
        }
    }
    return NULL;
}

bool scope_table::insert_in_scope(symbol_info* symbol)
{
    if (lookup_in_scope(symbol) != NULL)
    {
        return false;
    }
    int index = hash_function(symbol->get_name());
    table[index].push_back(symbol);
    return true;
}

bool scope_table::delete_from_scope(symbol_info* symbol)
{
    int index = hash_function(symbol->get_name());
    for (list<symbol_info *>::iterator it = table[index].begin(); it != table[index].end(); it++)
    {
        if ((*it)->get_name() == symbol->get_name())
        {
            table[index].erase(it);
            return true;
        }
    }
    return false;
}

void scope_table::print_scope_table(ofstream& outlog)
{
    outlog << "ScopeTable # "+ to_string(unique_id) << endl;

    //iterate through the current scope table and print the symbols and all relevant information
    for (int i = 0; i < bucket_count; i++)
    {
        if (!table[i].empty())
        {
            outlog << i << " --> " << endl;
            for (list<symbol_info *>::iterator it = table[i].begin(); it != table[i].end(); it++)
            {
                symbol_info *s = *it;
                outlog << "< " << s->get_name() << " : " << s->get_type() << " >" << endl;
                if (s->get_symbol_type() == "Variable")
                {
                    outlog << "Variable" << endl;
                    outlog << "Type: " << s->get_data_type() << endl;
                }
                else if (s->get_symbol_type() == "Array")
                {
                    outlog << "Array" << endl;
                    outlog << "Type: " << s->get_data_type() << endl;
                    outlog << "Size: " << s->get_array_size() << endl;
                }
                else if (s->get_symbol_type() == "Function Definition")
                {
                    outlog << "Function Definition" << endl;
                    outlog << "Return Type: " << s->get_return_type() << endl;
                    outlog << "Number of Parameters: " << s->get_param_count() << endl;
                    outlog << "Parameter Details: " << s->get_param_details() << endl;
                }
            }
            outlog << endl;
        }
    }
}

scope_table::~scope_table()
{
    for (int i = 0; i < bucket_count; i++)
    {
        for (list<symbol_info *>::iterator it = table[i].begin(); it != table[i].end(); it++)
        {
            delete (*it);
        }
        table[i].clear();
    }
}
