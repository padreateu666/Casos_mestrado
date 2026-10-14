R = 0.02;
Cx = 0.36;
Cy = 0.256;
Cz = 0.256; 

cl = 0.0026;

Point(1)={Cx, Cy, Cz, cl};
Point(2)={Cx+R, Cy, Cz, cl};
Point(3)={Cx, Cy+R, Cz, cl};
Point(4)={Cx, Cy-R, Cz, cl};

Circle(1)={2,1,4};
Circle(2)={3,1,2};

Extrude {{0, 1, 0}, {Cx, Cy, Cz}, Pi/2} {
  Line{1, 2};
}

Extrude {{0, 1, 0}, {Cx, Cy, Cz}, Pi/2} {
  Line{3, 6};
}

Extrude {{0, 1, 0}, {Cx, Cy, Cz}, Pi/2} {
  Line{9, 12};
}

Extrude {{0, 1, 0}, {Cx, Cy, Cz}, Pi/2} {
  Line{18, 15};
}

