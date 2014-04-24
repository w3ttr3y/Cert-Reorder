Cert-Reorder
============

A python script to re-order the certificates in a pen formatted file.  One of the applications we run requires that the certificates be in a particular order (server, intermediate, CA) and our CA provided the certificates in the opposite order (CA, intermediate, server) so I wrote this script to correct the ordering.

While the ultimate goal would be to have the ability to list the certificates in an arbitrary order, this currently is not supported.  Adding that functionality would be trivial, I had a perl script which would do just that, but the specific use case I wrote the script to solve, the certificates were always in CA, intermediate, server certificate and I needed them in the opposite order so I initially implemented a reversing operation `-r` and then later also  implemented an automatic option `-a`

##Usage

To reverse the certificate order in the pen file:
    ./cert-reorder.py -r certificatechain.pem

To analyze the certificates and put them in CA, intermediate, server order:
    ./cert-reorder.py -a certificatechain.pem
    
If you want to analyze the certificates and put them in server, intermediate, CA order you can use two invocations:
    ./cert-reorder.py -a certificatechain.pem | ./cert-reorder.py -r
    
If you want to verify the order of a certificate chain, you can use the -p option:
    ./cert-reorder.py -p certificatechain.pem
    
If you want to verify the order of the certificates after a command, you can save the results in a file and then use the previous command to print the common names of the certificates or you can just run the command and pipe the output back to cert-reorder.py
    ./cert-reorder.py -a certificatechain.pem | ./cert-reorder.py -p


###Program Usage Output
> usage: cert-reorder.py [-h] [-r | -p | -a] [file]
> 
> Manipulate the order of certificates in a pem style file
>
> positional arguments:
>   file
>
> optional arguments:
>  -h, --help     show this help message and exit
>  -r, --reverse  Reverse the order of certificates.
>  -p, --print
>  -a, --auto