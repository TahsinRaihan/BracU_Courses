%{

#include "symbol_table.h"

#define YYSTYPE symbol_info*

extern FILE *yyin;
int yyparse(void);
int yylex(void);
extern YYSTYPE yylval;

int lines = 1;

ofstream outlog;
ofstream outerror;

symbol_table *table;

vector<pair<string,int>> decl_id_list;
vector<pair<string,string>> func_param_list;
vector<vector<string>> call_arg_stack;
vector<symbol_info*> rejected_symbols;
symbol_info *current_func_symbol;
string current_func_name;
bool func_scope_pending = false;
int error_count = 0;

void print_error(string msg)
{
	outlog<<"At line no: "<<lines<<" "<<msg<<endl<<endl;
	outerror<<"At line no: "<<lines<<" "<<msg<<endl<<endl;
	error_count++;
}

void add_param(string type, string name)
{
	if(name != "")
	{
		for(unsigned int i = 0; i < func_param_list.size(); i++)
		{
			if(func_param_list[i].second == name)
			{
				print_error("Multiple declaration of variable "+name+" in parameter of "+current_func_name);
				break;
			}
		}
	}
	func_param_list.push_back(make_pair(type,name));
}

void yyerror(char *s)
{
	print_error((string)s);

	decl_id_list.clear();
	func_param_list.clear();
	call_arg_stack.clear();
}

%}

%token IF ELSE FOR WHILE DO BREAK INT CHAR FLOAT DOUBLE VOID RETURN SWITCH CASE DEFAULT CONTINUE PRINTLN ADDOP MULOP INCOP DECOP RELOP ASSIGNOP LOGICOP NOT LPAREN RPAREN LCURL RCURL LTHIRD RTHIRD COMMA SEMICOLON CONST_INT CONST_FLOAT ID

%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%%

start : program
	{
		outlog<<"At line no: "<<lines<<" start : program "<<endl<<endl;
		outlog<<"Symbol Table"<<endl<<endl;
		
		table->print_all_scopes(outlog);
	}
	;

program : program unit
	{
		outlog<<"At line no: "<<lines<<" program : program unit "<<endl<<endl;
		outlog<<$1->get_name()+"\n"+$2->get_name()<<endl<<endl;
		
		$$ = new symbol_info($1->get_name()+"\n"+$2->get_name(),"program");
	}
	| unit
	{
		outlog<<"At line no: "<<lines<<" program : unit "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;
		
		$$ = new symbol_info($1->get_name(),"program");
	}
	;

unit : variable_decl
	 {
		outlog<<"At line no: "<<lines<<" unit : variable_decl "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;
		
		$$ = new symbol_info($1->get_name(),"unit");
	 }
     | func_definition
     {
		outlog<<"At line no: "<<lines<<" unit : func_definition "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"unit");
	 }
     | error SEMICOLON
     {
		$$ = new symbol_info("","unit");
		yyerrok;
	 }
     ;

func_definition : type_specifier ID LPAREN
		{
			func_param_list.clear();
			current_func_name = $2->get_name();
			func_scope_pending = true;
		}
		param_list RPAREN
		{
			current_func_symbol = new symbol_info($2->get_name(),"ID");
			current_func_symbol->set_symbol_type("Function Definition");
			current_func_symbol->set_return_type($1->get_name());
			if(!table->insert(current_func_symbol))
			{
				print_error("Multiple declaration of function "+$2->get_name());
				rejected_symbols.push_back(current_func_symbol);
			}
			table->enter_scope(outlog);
			int p_count = 0;
			string p_details = "";
			for(unsigned int i = 0; i < func_param_list.size(); i++)
			{
				if(func_param_list[i].second != "")
				{
					symbol_info *param_sym = new symbol_info(func_param_list[i].second,"ID");
					param_sym->set_symbol_type("Variable");
					param_sym->set_data_type(func_param_list[i].first);
					if(!table->insert(param_sym))
					{
						delete param_sym;
					}
				}
				if(p_details != "")
				{
					p_details += ", ";
				}
				p_details += func_param_list[i].first;
				if(func_param_list[i].second != "")
				{
					p_details += " " + func_param_list[i].second;
				}
				current_func_symbol->add_param_type(func_param_list[i].first);
				p_count++;
			}
			current_func_symbol->set_param_count(p_count);
			current_func_symbol->set_param_details(p_details);
		}
		compound_statement
		{	
			outlog<<"At line no: "<<lines<<" func_definition : type_specifier ID LPAREN param_list RPAREN compound_statement "<<endl<<endl;
			outlog<<$1->get_name()<<" "<<$2->get_name()<<"("+$5->get_name()+")\n"<<$8->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name()+" "+$2->get_name()+"("+$5->get_name()+")\n"+$8->get_name(),"func_def");	
		}
		| type_specifier ID LPAREN
		{
			func_param_list.clear();
			current_func_name = $2->get_name();
			func_scope_pending = true;
		}
		RPAREN
		{
			current_func_symbol = new symbol_info($2->get_name(),"ID");
			current_func_symbol->set_symbol_type("Function Definition");
			current_func_symbol->set_return_type($1->get_name());
			if(!table->insert(current_func_symbol))
			{
				print_error("Multiple declaration of function "+$2->get_name());
				rejected_symbols.push_back(current_func_symbol);
			}
			table->enter_scope(outlog);
			current_func_symbol->set_param_count(0);
			current_func_symbol->set_param_details("");
		}
		compound_statement
		{
			
			outlog<<"At line no: "<<lines<<" func_definition : type_specifier ID LPAREN RPAREN compound_statement "<<endl<<endl;
			outlog<<$1->get_name()<<" "<<$2->get_name()<<"()\n"<<$7->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name()+" "+$2->get_name()+"()\n"+$7->get_name(),"func_def");	
		}
 		;

param_list : param_list COMMA type_specifier ID
		{
			outlog<<"At line no: "<<lines<<" param_list : param_list COMMA type_specifier ID "<<endl<<endl;
			outlog<<$1->get_name()<<","<<$3->get_name()<<" "<<$4->get_name()<<endl<<endl;
					
			$$ = new symbol_info($1->get_name()+","+$3->get_name()+" "+$4->get_name(),"param_list");
			
			add_param($3->get_name(),$4->get_name());
		}
		| param_list COMMA type_specifier
		{
			outlog<<"At line no: "<<lines<<" param_list : param_list COMMA type_specifier "<<endl<<endl;
			outlog<<$1->get_name()<<","<<$3->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name()+","+$3->get_name(),"param_list");
			
			add_param($3->get_name(),"");
		}
 		| type_specifier ID
 		{
			outlog<<"At line no: "<<lines<<" param_list : type_specifier ID "<<endl<<endl;
			outlog<<$1->get_name()<<" "<<$2->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name()+" "+$2->get_name(),"param_list");
			
			add_param($1->get_name(),$2->get_name());
		}
		| type_specifier
		{
			outlog<<"At line no: "<<lines<<" param_list : type_specifier "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"param_list");
			
			add_param($1->get_name(),"");
		}
 		;

compound_statement : LCURL
			{
				if(func_scope_pending)
				{
					func_scope_pending = false;
				}
				else
				{
					table->enter_scope(outlog);
				}
			}
			statements RCURL
			{ 
 		    	outlog<<"At line no: "<<lines<<" compound_statement : LCURL statements RCURL "<<endl<<endl;
				outlog<<"{\n"+$3->get_name()+"\n}"<<endl<<endl;
				
				$$ = new symbol_info("{\n"+$3->get_name()+"\n}","comp_stmnt");
				
				table->exit_scope(outlog);
 		    }
 		    | LCURL
 		    {
				if(func_scope_pending)
				{
					func_scope_pending = false;
				}
				else
				{
					table->enter_scope(outlog);
				}
			}
			RCURL
 		    { 
 		    	outlog<<"At line no: "<<lines<<" compound_statement : LCURL RCURL "<<endl<<endl;
				outlog<<"{\n}"<<endl<<endl;
				
				$$ = new symbol_info("{\n}","comp_stmnt");
				
				table->exit_scope(outlog);
 		    }
 		    ;
 		    
variable_decl : type_specifier declaration_list SEMICOLON
		 {
			outlog<<"At line no: "<<lines<<" variable_decl : type_specifier declaration_list SEMICOLON "<<endl<<endl;
			outlog<<$1->get_name()<<" "<<$2->get_name()<<";"<<endl<<endl;
			
			$$ = new symbol_info($1->get_name()+" "+$2->get_name()+";","var_dec");
			
			if($1->get_name() == "void")
			{
				print_error("variable type can not be void ");
			}
			
			string decl_type = $1->get_name() == "void" ? "error" : $1->get_name();

			for(unsigned int i = 0; i < decl_id_list.size(); i++)
			{
				symbol_info *var_sym = new symbol_info(decl_id_list[i].first,"ID");
				if(decl_id_list[i].second > 0)
				{
					var_sym->set_symbol_type("Array");
					var_sym->set_data_type(decl_type);
					var_sym->set_array_size(decl_id_list[i].second);
				}
				else
				{
					var_sym->set_symbol_type("Variable");
					var_sym->set_data_type(decl_type);
				}
				if(!table->insert(var_sym))
				{
					print_error("Multiple declaration of variable "+decl_id_list[i].first);
					symbol_info *existing = table->lookup_current_scope(decl_id_list[i].first);
					if(existing != NULL)
					{
						existing->set_effective_type(decl_type);
					}
					delete var_sym;
				}
			}
		 }
 		 ;

type_specifier : INT
		{
			outlog<<"At line no: "<<lines<<" type_specifier : INT "<<endl<<endl;
			outlog<<"int"<<endl<<endl;
			
			$$ = new symbol_info("int","type");
	    }
 		| FLOAT
 		{
			outlog<<"At line no: "<<lines<<" type_specifier : FLOAT "<<endl<<endl;
			outlog<<"float"<<endl<<endl;
			
			$$ = new symbol_info("float","type");
	    }
 		| VOID
 		{
			outlog<<"At line no: "<<lines<<" type_specifier : VOID "<<endl<<endl;
			outlog<<"void"<<endl<<endl;
			
			$$ = new symbol_info("void","type");
	    }
		| CHAR
 		{
			outlog<<"At line no: "<<lines<<" type_specifier : CHAR "<<endl<<endl;
			outlog<<"char"<<endl<<endl;

			$$ = new symbol_info("char","type");
	    }
 		| DOUBLE
 		{
			outlog<<"At line no: "<<lines<<" type_specifier : DOUBLE "<<endl<<endl;
			outlog<<"double"<<endl<<endl;

			$$ = new symbol_info("double","type");
	    }
 		;

declaration_list : declaration_list COMMA ID
		  {
 		  	outlog<<"At line no: "<<lines<<" declaration_list : declaration_list COMMA ID "<<endl<<endl;
 		  	outlog<<$1->get_name()+","<<$3->get_name()<<endl<<endl;

			decl_id_list.push_back(make_pair($3->get_name(),0));

			$$ = new symbol_info($1->get_name()+","+$3->get_name(),"declaration_list");
 		  }
 		  | declaration_list COMMA ID LTHIRD CONST_INT RTHIRD
 		  {
 		  	outlog<<"At line no: "<<lines<<" declaration_list : declaration_list COMMA ID LTHIRD CONST_INT RTHIRD "<<endl<<endl;
 		  	outlog<<$1->get_name()+","<<$3->get_name()<<"["<<$5->get_name()<<"]"<<endl<<endl;

			decl_id_list.push_back(make_pair($3->get_name(),atoi($5->get_name().c_str())));

			$$ = new symbol_info($1->get_name()+","+$3->get_name()+"["+$5->get_name()+"]","declaration_list");
 		  }
 		  |ID
 		  {
 		  	outlog<<"At line no: "<<lines<<" declaration_list : ID "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"declaration_list");

			decl_id_list.clear();
			decl_id_list.push_back(make_pair($1->get_name(),0));
 		  }
 		  | ID LTHIRD CONST_INT RTHIRD
 		  {
 		  	outlog<<"At line no: "<<lines<<" declaration_list : ID LTHIRD CONST_INT RTHIRD "<<endl<<endl;
			outlog<<$1->get_name()<<"["<<$3->get_name()<<"]"<<endl<<endl;

			$$ = new symbol_info($1->get_name()+"["+$3->get_name()+"]","declaration_list");

			decl_id_list.clear();
			decl_id_list.push_back(make_pair($1->get_name(),atoi($3->get_name().c_str())));
 		  }
 		  ;
 		  

statements : statement
	   {
	    	outlog<<"At line no: "<<lines<<" statements : statement "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"stmnts");
	   }
	   | statements statement
	   {
	    	outlog<<"At line no: "<<lines<<" statements : statements statement "<<endl<<endl;
			outlog<<$1->get_name()<<"\n"<<$2->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name()+"\n"+$2->get_name(),"stmnts");
	   }
	   ;
	   
statement : variable_decl
	  {
	    	outlog<<"At line no: "<<lines<<" statement : variable_decl "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"stmnt");
	  }
	  | func_definition
	  {
	  		outlog<<"At line no: "<<lines<<" statement : func_definition "<<endl<<endl;
            outlog<<$1->get_name()<<endl<<endl;

            $$ = new symbol_info($1->get_name(),"stmnt");
	  		
	  }
	  | expression_statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : expression_statement "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"stmnt");
	  }
	  | compound_statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : compound_statement "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"stmnt");
	  }
	  | FOR LPAREN expression_statement expression_statement expression RPAREN statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement "<<endl<<endl;
			outlog<<"for("<<$3->get_name()<<$4->get_name()<<$5->get_name()<<")\n"<<$7->get_name()<<endl<<endl;
			
			$$ = new symbol_info("for("+$3->get_name()+$4->get_name()+$5->get_name()+")\n"+$7->get_name(),"stmnt");
	  }
	  | IF LPAREN expression RPAREN statement %prec LOWER_THAN_ELSE
	  {
	    	outlog<<"At line no: "<<lines<<" statement : IF LPAREN expression RPAREN statement "<<endl<<endl;
			outlog<<"if("<<$3->get_name()<<")\n"<<$5->get_name()<<endl<<endl;
			
			$$ = new symbol_info("if("+$3->get_name()+")\n"+$5->get_name(),"stmnt");
	  }
	  | IF LPAREN expression RPAREN statement ELSE statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : IF LPAREN expression RPAREN statement ELSE statement "<<endl<<endl;
			outlog<<"if("<<$3->get_name()<<")\n"<<$5->get_name()<<"\nelse\n"<<$7->get_name()<<endl<<endl;
			
			$$ = new symbol_info("if("+$3->get_name()+")\n"+$5->get_name()+"\nelse\n"+$7->get_name(),"stmnt");
	  }
	  | WHILE LPAREN expression RPAREN statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : WHILE LPAREN expression RPAREN statement "<<endl<<endl;
			outlog<<"while("<<$3->get_name()<<")\n"<<$5->get_name()<<endl<<endl;

			$$ = new symbol_info("while("+$3->get_name()+")\n"+$5->get_name(),"stmnt");
	  }
	  | DO statement WHILE LPAREN expression RPAREN SEMICOLON
	  {
	    	outlog<<"At line no: "<<lines<<" statement : DO statement WHILE LPAREN expression RPAREN SEMICOLON "<<endl<<endl;
			outlog<<"do\n"<<$2->get_name()<<"\nwhile("<<$5->get_name()<<");"<<endl<<endl;

			$$ = new symbol_info("do\n"+$2->get_name()+"\nwhile("+$5->get_name()+");","stmnt");
	  }
	  | BREAK SEMICOLON
	  {
	    	outlog<<"At line no: "<<lines<<" statement : BREAK SEMICOLON "<<endl<<endl;
			outlog<<"break;"<<endl<<endl;

			$$ = new symbol_info("break;","stmnt");
	  }
	  | CONTINUE SEMICOLON
	  {
	    	outlog<<"At line no: "<<lines<<" statement : CONTINUE SEMICOLON "<<endl<<endl;
			outlog<<"continue;"<<endl<<endl;

			$$ = new symbol_info("continue;","stmnt");
	  }
	  | PRINTLN LPAREN ID RPAREN SEMICOLON
	  {
	    	outlog<<"At line no: "<<lines<<" statement : PRINTLN LPAREN ID RPAREN SEMICOLON "<<endl<<endl;
			outlog<<"printf("<<$3->get_name()<<");"<<endl<<endl; 
			
			$$ = new symbol_info("printf("+$3->get_name()+");","stmnt");
			
			symbol_info *lookup_key4 = new symbol_info($3->get_name(),"ID");
			symbol_info *printf_sym_found = table->lookup(lookup_key4);
			delete lookup_key4;
			
			if(printf_sym_found == NULL)
			{
				print_error("Undeclared variable "+$3->get_name());
			}
	  }
	  | RETURN expression SEMICOLON
	  {
	    	outlog<<"At line no: "<<lines<<" statement : RETURN expression SEMICOLON "<<endl<<endl;
			outlog<<"return "<<$2->get_name()<<";"<<endl<<endl;

			$$ = new symbol_info("return "+$2->get_name()+";","stmnt");
	  }
	  | error SEMICOLON
	  {
			$$ = new symbol_info(";","stmnt");
			yyerrok;
	  }
	  ;
	  
expression_statement : SEMICOLON
			{
				outlog<<"At line no: "<<lines<<" expression_statement : SEMICOLON "<<endl<<endl;
				outlog<<";"<<endl<<endl;
				
				$$ = new symbol_info(";","expr_stmt");
	        }			
			| expression SEMICOLON 
			{
				outlog<<"At line no: "<<lines<<" expression_statement : expression SEMICOLON "<<endl<<endl;
				outlog<<$1->get_name()<<";"<<endl<<endl;
				
				$$ = new symbol_info($1->get_name()+";","expr_stmt");
	        }
			;
	  
variable : ID 	
      {
	    outlog<<"At line no: "<<lines<<" variable : ID "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;
			
		symbol_info *lookup_key = new symbol_info($1->get_name(),"ID");
		symbol_info *found_sym = table->lookup(lookup_key);
		delete lookup_key;
		
		if(found_sym == NULL)
		{
			print_error("Undeclared variable "+$1->get_name());
			$$ = new symbol_info($1->get_name(),"varbl","error");
		}
		else if(found_sym->get_symbol_type() == "Array")
		{
			print_error("variable is of array type : "+$1->get_name());
			$$ = new symbol_info($1->get_name(),"varbl","error");
			$$->set_symbol_type("Array");
		}
		else if(found_sym->get_symbol_type() == "Function Definition")
		{
			$$ = new symbol_info($1->get_name(),"varbl",found_sym->get_return_type());
		}
		else
		{
			$$ = new symbol_info($1->get_name(),"varbl",found_sym->get_effective_type());
		}
		
	 }	
	 | ID LTHIRD expression RTHIRD 
	 {
	 	outlog<<"At line no: "<<lines<<" variable : ID LTHIRD expression RTHIRD "<<endl<<endl;
		outlog<<$1->get_name()<<"["<<$3->get_name()<<"]"<<endl<<endl;
		
		symbol_info *lookup_key2 = new symbol_info($1->get_name(),"ID");
		symbol_info *found_sym2 = table->lookup(lookup_key2);
		delete lookup_key2;
		
		if(found_sym2 == NULL)
		{
			print_error("Undeclared variable "+$1->get_name());
			$$ = new symbol_info($1->get_name()+"["+$3->get_name()+"]","varbl","error");
		}
		else if(found_sym2->get_symbol_type() != "Array")
		{
			print_error("variable is not of array type : "+$1->get_name());
			$$ = new symbol_info($1->get_name()+"["+$3->get_name()+"]","varbl",found_sym2->get_effective_type());
		}
		else
		{
			if($3->get_data_type() != "int" || found_sym2->get_effective_type() != "int")
			{
				print_error("array index is not of integer type : "+$1->get_name());
			}
			$$ = new symbol_info($1->get_name()+"["+$3->get_name()+"]","varbl",found_sym2->get_effective_type());
		}
	 }
	 ;
	 
expression : logic_expression
	   {
	    	outlog<<"At line no: "<<lines<<" expression : logic_expression "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"expr",$1->get_data_type());
	   }
	   | variable ASSIGNOP logic_expression 	
	   {
	    	outlog<<"At line no: "<<lines<<" expression : variable ASSIGNOP logic_expression "<<endl<<endl;
			outlog<<$1->get_name()<<"="<<$3->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+"="+$3->get_name(),"expr",$1->get_data_type());
	   }
	   ;
			
logic_expression : rel_expression
	     {
	    	outlog<<"At line no: "<<lines<<" logic_expression : rel_expression "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"lgc_expr",$1->get_data_type());
	     }	
		 | rel_expression LOGICOP rel_expression 
		 {
	    	outlog<<"At line no: "<<lines<<" logic_expression : rel_expression LOGICOP rel_expression "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<$3->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"lgc_expr","int");
			
			if($1->get_data_type() == "void" || $3->get_data_type() == "void")
			{
				print_error("Void function used in expression");
			}
	     }	
		 ;
			
rel_expression	: simple_expression
		{
	    	outlog<<"At line no: "<<lines<<" rel_expression : simple_expression "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"rel_expr",$1->get_data_type());
	    }
		| simple_expression RELOP simple_expression
		{
	    	outlog<<"At line no: "<<lines<<" rel_expression : simple_expression RELOP simple_expression "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<$3->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"rel_expr","int");
			
			if($1->get_data_type() == "void" || $3->get_data_type() == "void")
			{
				print_error("Void function used in expression");
			}
	    }
		;
				
simple_expression : term
          {
	    	outlog<<"At line no: "<<lines<<" simple_expression : term "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"simp_expr",$1->get_data_type());
			
	      }
		  | simple_expression ADDOP term 
		  {
	    	outlog<<"At line no: "<<lines<<" simple_expression : simple_expression ADDOP term "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<$3->get_name()<<endl<<endl;
			
			if($1->get_data_type() == "float" || $3->get_data_type() == "float")
			{
				$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"simp_expr","float");
			}
			else
			{
				$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"simp_expr","int");
			}
	      }
		  ;
					
term :	unary_expression
     {
	    	outlog<<"At line no: "<<lines<<" term : unary_expression "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"term",$1->get_data_type());
			
	 }
     |  term MULOP unary_expression
     {
	    	outlog<<"At line no: "<<lines<<" term : term MULOP unary_expression "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<$3->get_name()<<endl<<endl;
			
			if($2->get_name() == "%")
			{
				$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"term","int");
			}
			else if($2->get_name() == "/")
			{
				if($1->get_data_type() == "float" || $3->get_data_type() == "float")
				{
					$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"term","float");
				}
				else
				{
					$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"term","int");
				}
			}
			else
			{
				if($1->get_data_type() == "float" || $3->get_data_type() == "float")
				{
					$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"term","float");
				}
				else
				{
					$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"term","int");
				}
			}
			
	 }
     ;

unary_expression : ADDOP unary_expression
		 {
	    	outlog<<"At line no: "<<lines<<" unary_expression : ADDOP unary_expression "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name()+$2->get_name(),"un_expr",$2->get_data_type());
			
			if($2->get_data_type() == "void")
			{
				print_error("Void function used in expression");
			}
	     }
		 | NOT unary_expression 
		 {
	    	outlog<<"At line no: "<<lines<<" unary_expression : NOT unary_expression "<<endl<<endl;
			outlog<<"!"<<$2->get_name()<<endl<<endl;
			
			$$ = new symbol_info("!"+$2->get_name(),"un_expr","int");
			
			if($2->get_data_type() == "void")
			{
				print_error("Void function used in expression");
			}
	     }
		 | factor_info  
		 {
	    	outlog<<"At line no: "<<lines<<" unary_expression : factor_info "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;
			
			$$ = new symbol_info($1->get_name(),"un_expr",$1->get_data_type());
			if($1->get_symbol_type() == "Array")
			{
				$$->set_symbol_type("Array");
			}
	     }
		 ;
factor_info : factor	{
	    outlog<<"At line no: "<<lines<<" factor_info : factor "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;
			
		$$ = new symbol_info($1->get_name(),"fctr_info",$1->get_data_type());
		if($1->get_symbol_type() == "Array")
		{
			$$->set_symbol_type("Array");
		}
	}
	;

factor	: variable
    {
	    outlog<<"At line no: "<<lines<<" factor : variable "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;
			
		$$ = new symbol_info($1->get_name(),"fctr",$1->get_data_type());
		if($1->get_symbol_type() == "Array")
		{
			$$->set_symbol_type("Array");
		}
	}
	| ID LPAREN
	{
		call_arg_stack.push_back(vector<string>());
	}
	argument_list RPAREN
	{
	    outlog<<"At line no: "<<lines<<" factor : ID LPAREN argument_list RPAREN "<<endl<<endl;
		outlog<<$1->get_name()<<"("<<$4->get_name()<<")"<<endl<<endl;

		$$ = new symbol_info($1->get_name()+"("+$4->get_name()+")","fctr");
		
		symbol_info *lookup_key3 = new symbol_info($1->get_name(),"ID");
		symbol_info *func_sym_found = table->lookup(lookup_key3);
		delete lookup_key3;
		
		vector<string> this_call_arg_types;
		if(!call_arg_stack.empty())
		{
			this_call_arg_types = call_arg_stack.back();
			call_arg_stack.pop_back();
		}
		
		if(func_sym_found == NULL)
		{
			print_error("Undeclared function: "+$1->get_name());
			$$->set_data_type("error");
		}
		else if(func_sym_found->get_symbol_type() != "Function Definition")
		{
			print_error($1->get_name()+" is not a function");
			$$->set_data_type("error");
		}
		else
		{
			vector<string> expected_param_types = func_sym_found->get_param_type_list();
			string func_ret = func_sym_found->get_return_type();
			if(expected_param_types.size() != this_call_arg_types.size())
			{
				print_error("Inconsistencies in number of arguments in function call: "+$1->get_name());
			}
			else if(expected_param_types.size() == 0)
			{
				if(func_ret == "void")
				{
					print_error("Void function used in expression");
					func_ret = "error";
				}
			}
			else
			{
				for(unsigned int ai = 0; ai < expected_param_types.size(); ai++)
				{
					if(this_call_arg_types[ai] == "error" || this_call_arg_types[ai] != expected_param_types[ai] || func_ret == "void")
					{
						print_error("argument "+to_string(ai+1)+" type mismatch in function call: "+$1->get_name());
					}
				}
			}
			$$->set_data_type(func_ret);
		}
	}
	| LPAREN expression RPAREN
	{
	   	outlog<<"At line no: "<<lines<<" factor : LPAREN expression RPAREN "<<endl<<endl;
		outlog<<"("<<$2->get_name()<<")"<<endl<<endl;
		
		$$ = new symbol_info("("+$2->get_name()+")","fctr",$2->get_data_type());
	}
	| CONST_INT 
	{
	    outlog<<"At line no: "<<lines<<" factor : CONST_INT "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;
			
		$$ = new symbol_info($1->get_name(),"fctr","int");
	}
	| CONST_FLOAT
	{
	    outlog<<"At line no: "<<lines<<" factor : CONST_FLOAT "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;
			
		$$ = new symbol_info($1->get_name(),"fctr","float");
	}
	| variable INCOP 
	{
	    outlog<<"At line no: "<<lines<<" factor : variable INCOP "<<endl<<endl;
		outlog<<$1->get_name()<<"++"<<endl<<endl;
			
		$$ = new symbol_info($1->get_name()+"++","fctr",$1->get_data_type());
	}
	| variable DECOP
	{
	    outlog<<"At line no: "<<lines<<" factor : variable DECOP "<<endl<<endl;
		outlog<<$1->get_name()<<"--"<<endl<<endl;
			
		$$ = new symbol_info($1->get_name()+"--","fctr",$1->get_data_type());
	}
	;
	
argument_list : arguments
			  {
					outlog<<"At line no: "<<lines<<" argument_list : arguments "<<endl<<endl;
					outlog<<$1->get_name()<<endl<<endl;
						
					$$ = new symbol_info($1->get_name(),"arg_list");
			  }
			  |
			  {
					outlog<<"At line no: "<<lines<<" argument_list :  "<<endl<<endl;
					outlog<<""<<endl<<endl;
						
					$$ = new symbol_info("","arg_list");
			  }
			  ;
	
arguments : arguments COMMA logic_expression
		  {
				outlog<<"At line no: "<<lines<<" arguments : arguments COMMA logic_expression "<<endl<<endl;
				outlog<<$1->get_name()<<","<<$3->get_name()<<endl<<endl;
						
				$$ = new symbol_info($1->get_name()+","+$3->get_name(),"arg");

				if(!call_arg_stack.empty()) call_arg_stack.back().push_back($3->get_data_type());
		  }
	      | logic_expression
	      {
				outlog<<"At line no: "<<lines<<" arguments : logic_expression "<<endl<<endl;
				outlog<<$1->get_name()<<endl<<endl;
						
				$$ = new symbol_info($1->get_name(),"arg");

				if(!call_arg_stack.empty()) call_arg_stack.back().push_back($1->get_data_type());
		  }
	      ;
 

%%

int main(int argc, char *argv[])
{
	if(argc != 2) 
	{
		cout<<"Please input file name"<<endl;
		return 0;
	}
	yyin = fopen(argv[1], "r");
	outlog.open("22201344_log.txt", ios::trunc);
	outerror.open("22201344_error.txt", ios::trunc);
	
	if(yyin == NULL)
	{
		cout<<"Couldn't open file"<<endl;
		return 0;
	}
	table = new symbol_table(10);
	outlog<<"New ScopeTable with ID 1 created"<<endl<<endl;

	yyparse();
	
	outlog<<endl<<"Total lines: "<<lines<<endl;
	outlog<<"Total errors: "<<error_count<<endl;
	outerror<<"Total errors: "<<error_count<<endl;
	
	outlog.close();
	outerror.close();
	
	fclose(yyin);

	delete table;

	for(unsigned int i = 0; i < rejected_symbols.size(); i++)
	{
		delete rejected_symbols[i];
	}

	return 0;
}