#include <iostream>
#include  <fstream>
#include "pin.H"

static UINT64 icount = 0;
static bool icount_overflow = false;
ofstream o(".pintester.log");

VOID docount() {
	if (!icount) {
		if (icount_overflow) o << icount-1 << endl;
		else icount_overflow = true;
	}
	icount++;
}

const char * StripPath(const char * path) {
	const char * file = strrchr(path, '/');
	if (file)
		return file+1;
	else
		return path;
}

VOID Routine(RTN rtn, VOID *v) {
	string image = StripPath(IMG_Name(SEC_Img(RTN_Sec(rtn))).c_str());
	string rtname = RTN_Name(rtn);
	//if (image != ".qtest.out") return;
	//if (rtname[0] == '.' || rtname[0] == '_') return;
	//o << image << rtname << endl;
	RTN_Open(rtn);
	for (INS ins = RTN_InsHead(rtn); INS_Valid(ins); ins = INS_Next(ins))
		INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)docount, IARG_END);
	RTN_Close(rtn);
}

VOID Fini(INT32 code, VOID *v) {
	o << icount << endl;
	o.close();
}

int main(int argc, char * argv[]) {
	PIN_InitSymbols();
	o.setf(ios::showbase);
	if (PIN_Init(argc, argv)) return -1;
	RTN_AddInstrumentFunction(Routine, 0);
	PIN_AddFiniFunction(Fini, 0);
	PIN_StartProgram();
	return 0;
}
