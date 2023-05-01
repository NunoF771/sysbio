
# Import Biopython tools for running remote BLASTX
from Bio.Blast import NCBIWWW # This allows us to run remote BLAST searches 

def remote_blast(fasta_file,blast_type):
    if blast_type == 'protein':

        with open(fasta_file, "r") as f: # Get our sequence data
            protein_sequences = f.read()
            f.close()

        result_handle_prot = NCBIWWW.qblast("blastp", "nr", protein_sequences, entrez_query='Homo sapiens [organism]', format_type="XML") # Perform the BLAST search on the nr database, filtered for homo sapiens

        with open("blastp_results.xml", "w") as f: # Save our blast results
            f.write(result_handle_prot.read())

        result_handle_prot.close()

    elif blast_type == 'nucleotide':

        with open(fasta_file, "r") as f:
            nucleotide_sequences = f.read()
            f.close()

        result_handle_nuc = NCBIWWW.qblast("blastn", "nr", nucleotide_sequences, entrez_query='Homo sapiens [organism]', format_type="XML")

        with open("blastn_results.xml", "w") as f:
            f.write(result_handle_nuc.read())

        result_handle_nuc.close()

if __name__ == '__main__':
    remote_blast('protein_sequences.fasta','protein')
    remote_blast('nucleotide_sequences.fasta','nucleotide')
     
    


            
