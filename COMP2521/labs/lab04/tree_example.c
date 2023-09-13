List TreeSearchBetween(Tree t, Record lower, Record upper) {
    List l = ListNew();
    doTreeSearchBetween(t, t->root, lower, upper, l);
    return l;
}



static void doTreeSearchBetween(Tree t, Node n, Record lower,
                                Record upper, List l) {
    if (n == NULL) {
        return;
    }

    if (t->compare(n->rec, lower) < 0) {
        doTreeSearchBetween(t, n->right, lower, upper, l);
    } else if (t->compare(n->rec, upper) > 0) {
        doTreeSearchBetween(t, n->left, lower, upper, l);
    } else {
        doTreeSearchBetween(t, n->left, lower, upper, l);
        ListAppend(l, n->rec);
        doTreeSearchBetween(t, n->right, lower, upper, l);
    }
}