#include <iostream>
#include <map>
#include <vector>
#include <elfio/elfio.hpp>

using namespace std;
using namespace ELFIO;

typedef unsigned long ulong;
typedef pair<unsigned long, unsigned long> range_pair;
typedef vector<range_pair, unsigned long> range_list;


vector<string> functions;
int num_func = 0;
// 

//modify this offset
#define SECTION_OFFSET 246

struct tab_entry {
	string name;
	Elf64_Addr val;
	Elf_Xword size;
	unsigned char bind;
	unsigned char type;
	Elf_Half section_index;
	unsigned char other;
	tab_entry() {
		name = "";
		val = 0;
		size = 0;
		bind = 0;
		type = 0;
		section_index = 0;
		other = 0;
	}
	tab_entry(string nm, Elf64_Addr vl, Elf_Xword sz, unsigned char bnd, unsigned char tp, 
		Elf_Half si, unsigned char ot) : name(nm), val(vl), size(sz), bind(bnd), type(tp), 
		section_index(si), other(ot) {

		}
};




void create_symtab(const elfio& reader, map<string, tab_entry>& sym_tab, int& sym_tab_ind) {
	int sec_num = reader.sections.size();
	
	for (int i = 0; i < sec_num; ++i)
	{
		section *psec = reader.sections[i];
		if (psec->get_type() == SHT_SYMTAB) {
			sym_tab_ind = i;
			const symbol_section_accessor symbol(reader, psec);
			for (int j = 0; j < symbol.get_symbols_num(); j++){
				string name;
				Elf64_Addr val;
				Elf_Xword size;
				unsigned char bind;
				unsigned char type;
				Elf_Half section_index;
				unsigned char other;
				symbol.get_symbol(j, name, val, size, bind, type, section_index, other);
				// cout << name << " " << size << endl;
				tab_entry entry(name, val, size, bind, type, section_index, other);
				sym_tab[name] = entry;
			}
		}
	}

}



void pseudo_trace(map<string, ulong>& name_addr) {
	FILE *file = fopen("rearranged_symbols","r");
	char temp_string[100];
	ulong address = 0;

	// ifstream in;
	// in.open("rearranged_symbols");

	// while (in.good()) {
	// 	string temp;
	// 	ulong address;

	// }

	while (fscanf(file, "%lx %s", &address, temp_string) != EOF) {
		// char* temp_end = strchr(temp_string, '\n');
		// if (temp_end) {

		string temp(temp_string);
		name_addr[temp] = address;
		// }
	}
	return;
}

int main() {
	elfio reader, writer;
	int sym_sec_ind;
	// string dump_filename = "call_sites";

	// read_trace();
	map<string, tab_entry> sym_tab;
	
	reader.load("rearranged_binary");
	// string_section_accessor *str_sec;
	//store the symbol table in a map class for faster lookups later
	create_symtab(reader, sym_tab, sym_sec_ind);

	

	cout << "Symbols rearranged" << endl;

	//change the symbol table here

	int num_entries = reader.sections[sym_sec_ind]->get_size() / 24;

	string sym_data(reader.sections[sym_sec_ind]->get_data(), 
		reader.sections[sym_sec_ind]->get_data() + reader.sections[sym_sec_ind]->get_size());

	Elf64_Sym *symbol = (Elf64_Sym *)reader.sections[sym_sec_ind]->get_data();

	

	//pseudo symbol updates
	map<string, ulong> pseudo_map;
	pseudo_trace(pseudo_map);
	// cout << "SHIT";;
	// cout << num_entries;
	for (auto it : pseudo_map) {
		// cout << "ALKJsdkls";
		for (int i = 0; i < num_entries; i++) {
			// cout << sym_tab[it.first].val << "," << symbol[i].st_value << endl;
			if (sym_tab[it.first].val == symbol[i].st_value) {
				// cout << "HAHAHA";
				symbol[i].st_value = it.second;
				break;
			}
		}
	}

	
	reader.save("final_binary");

	return 0;
}