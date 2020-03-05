package model;

import java.util.ArrayList;

public class Filtering {
    public double[][] Tm;
    public double[][][] Om;
    private int rows;
    private int cols;

    public Filtering(int rows, int cols) {
        Tm = new double[rows*cols*4][rows*cols*4];
        Om = new double[rows*cols+1][rows*cols*4][rows*cols*4];

        this.rows = rows;
        this.cols = cols;

        calcTm();
        calcOm();
    }

    private void calcTm() {
        for (int cr = 0; cr < rows; cr++) {
            for (int cc = 0; cc < cols; cc++){
                for (int ch = 0; ch < 4; ch++) {
                    for (int nr = 0; nr < rows; nr++) {
                        for (int nc = 0; nc < cols; nc++){
                            for (int nh = 0; nh < 4; nh++){
                                Tm[cr+cc+ch][nc+nr+nh] = getT(cr, cc, ch, nr, nc, nh);
                            }
                        }
                    }
                }
            }
        }
    }

    public double getT(int x, int y, int h, int nX, int nY, int nH) {
        int distance = Math.abs(nX-x) + Math.abs(nY-y);
        if (distance != 1){
            return 0;
        }
        else {
            ArrayList<Integer> pd = getPosibleDirections(x,y);
            if (pd.size() == 4){
                if (h == nH){
                    return 0.7;
                }
                else {
                    return 0.1;
                }
            }
            else if (pd.size() == 3){
                if (facingWall(x, y, h)){
                    return 0.33;
                }
                else if (h == nH){
                    return 0.7;
                }
                else {
                    return 0.15;
                }
            }
            else {
                if (facingWall(x, y, h)){
                    return 0.5;
                }
                else if (h == nH){
                    return 0.7;
                }
                else {
                    return 0.30;
                }
            }
        }
    }

    private boolean facingWall(int x, int y, int h){
        switch (h) {
            case 0: y -= 1;
                break;
            case 1: x += 1;
                break;
            case 2: y += 1;
                break;
            case 3: x -= 1;
                break;
        }
        if (x < 0 || y < 0 || x > cols - 1 || y > rows -1){
            return true;
        }
        return false;
    }

    private ArrayList<Integer> getPosibleDirections(int x, int y){
        ArrayList<Integer> dirs = new ArrayList<Integer>();
        // check up
        if (y - 1 > -1){
            dirs.add(0);
        }
        // check right
        if (x + 1 < cols){
            dirs.add(1);
        }
        // check down
        if (y + 1 < rows){
            dirs.add(2);
        }
        // check left
        if (x - 1 > -1){
            dirs.add(3);
        }

        return dirs;
    }

    private void calcOm() {

    }
}
