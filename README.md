# Efficient gradient projections on ℓ1-ball for full sparse data
Implementation of algorithms described at paper "Efficient Projections onto the ℓ1-Ball for Learning in High Dimensions" 
by J.Duchi, S.Shalev-Shwartz, Y.Singer and T.Chandra:

https://stanford.edu/~jduchi/projects/DuchiShSiCh08.pdf

Contains two methods:
* Linear-time (in worst case) projection of vector with n dimensions on ℓ1-ball placed at origin with known radius z. 
Quite easy for understand and do not needs information about gradient procedure. Checks if vector inside the ball, and if
not - projects on simplex mirrored to R+^n vector v, and then mirror it back to the initial space.
* O(k\*log(n)) time projection algorithm for sparse data where k is amount of deletes/inserts of changed components 
for next iteration step. Works with Red-Black tree for intensive delete/insert operations which has fast update of amount 
and sum of elements in right and left subtrees after each delete/insert. More effective when used in pair with some
optimization method (otherwise, O(k\*log(n)) time estimate won't work).

To use first method:
* Just import projecting_linear.project_linear(v,z) function with vector v and scalar ℓ1-constraint z. Function will return
projected vector. Currently uses numpy library, though will be removed lately, as it is not needed for this algorithm.

Second method currently is in develop.

TODO: 
* Test sparse projection with some iterative procedure.
* Extend usage on transport flows.