Challenges
==
**Author**: Juliano Garcia de Oliveira
- Mini EP 01: exploring cache locality
	This program hows the time difference in two routines that use the cache levels differently. The code creates a 15000x15000 matrix, which is initialized with random values from 0 to N*N.
	Each routine search run through all elements of the matrix, and make additions in a counter, and accessing the elements of the matrix (in a *garbage* variable).

	The optimized version run through the matrix in a row major order, and the other in column major order. The difference obtained is due to the way that the memory is stored in the cache, making column major order much more efficient.

<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/4/4d/Row_and_column_major_order.svg"/>
</p>
