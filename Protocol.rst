 A typical WSGI request translate to:

header (4 bytes, size is in little endian) :

{{{
|flag1|pktsize_byte1|pktsize_byte2|flag2|
}}}

WSGI env vars follow (this is a block of the size specified in the header, string size is 16 bit little endian):

{{{
|keysize_byte1|keysize_byte2|...string...|valuesize_byte1|valuesize_byte2|...string...|keysize_byte1|keysize_byte2|...string..................
}}}