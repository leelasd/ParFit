void rdfile(int, int);
void rdpcm(int,int);
void pcmfin(int,int);
void pcmfout(int);
void gettoken(void);
int make_atom(int,float,float,float,char *);
void initialize(void);
void make_bond(int,int,int);
void message_alert(char *, char *);
FILE * fopen_path ( char * , char * , char * ) ;
int mm3_mmxtype(int);
int mmff_mmxtype(int);
void set_atomtype(int,int,int,int,int,int);
int FetchRecord(FILE *, char *);
void zero_data(void);
void read_datafiles(char *);
void read_atomtypes(int);
void get_atomname(int,char *);
void clean_string(char *);
void hdel(int);
