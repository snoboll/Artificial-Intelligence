package model;

import control.EstimatorInterface;

import java.lang.reflect.Array;
import java.util.Random;
import java.util.ArrayList;


public class Localizer implements EstimatorInterface {

    private int rows, cols, head;
    private int row;
    private int col;
    private int currentHeading;

    private int[] currentReading;

    private static final int NORTH = 0;
    private static final int EAST = 1;
    private static final int SOUTH = 2;
    private static final int WEST = 3;

    private double[][] transitionMatrix;
    private double[][] observationVectors;

    private static int[][] offset1 = { { -1, -1 }, { -1, 0 }, { -1, 1 }, { 0, -1 }, { 0, 1 }, { 1, -1 }, { 1, 0 }, { 1, 1 } };
    private static int[][] offset2 = { { -2, -2 }, { -2, -1 }, { -2, 0 }, { -2, 1 }, { -2, 2 },
            { -1, -2 }, { -1, 2 }, { 0, -2 }, { 0, 2 }, { 1, -2 }, { 1, 2 },
            { 2, -2 }, { 2, -1 }, { 2, 0 }, { 2, 1 }, { 2, 2 } };

    public Localizer(int rows, int cols, int head) {
        this.rows = rows;
        this.cols = cols;
        this.head = head;

        row = 0;
        col = 0;

        currentHeading = EAST;

        transitionMatrix = new double[rows*cols*head][rows*cols*head];
        makeT();

        observationVectors = new double[rows*cols+1][rows*cols];
        makeO();

        printMat(observationVectors, rows*cols+1, rows*cols);
    }

    public int getNumRows() {
        return rows;
    }

    public int getNumCols() {
        return cols;
    }

    public int getNumHead() {
        return head;
    }


    /*
     * makes the transitionMatrix
     */
    public void makeT(){
        for (int frow = 0; frow < rows; frow++){
            for (int fcol = 0; fcol < cols; fcol++){
                for (int fhead = 0; fhead < head; fhead++){
                    for (int trow = 0; trow < rows; trow++){
                        for (int tcol = 0; tcol < cols; tcol++){
                            for (int thead = 0; thead < head; thead++){
                                transitionMatrix[frow*rows*head+fcol*head+fhead][trow*rows*head+tcol*head+thead] = Tprob(frow, fcol, fhead, trow, tcol, thead);
                            }
                        }
                    }
                }
            }
        }
    }

    /*
     * makes the observationMatrix
     */
    private void makeO(){
        // rr = reading row, rc = reading col
        for (int rr = 0; rr < rows; rr++){
            for (int rc = 0; rc < cols; rc++){
                for (int r = 0; r < rows; r++){
                    for (int c = 0; c < cols; c++){
                        observationVectors[rr*cols + rc][r*rows + c] = Oprob(rr, rc, r, c);

                    }
                }
                // setting up the nothing reading values for each position
                observationVectors[rows*cols][rr*cols + rc] = nothingProb(rr, rc);
            }
        }
    }

    private double nothingProb(int r, int c){
        double ret = 0.9;
        for (int i = 0; i<rows; i++){
            for(int j = 0; j<cols; j++){
                if(Math.sqrt(Math.pow(r - i, 2) + Math.pow(c - j, 2)) < 1){
                    ret-=0.1;
                }else if(Math.sqrt(Math.pow(r - i, 2) + Math.pow(c - j, 2)) < 2){
                    ret-=0.05;
                }else if(Math.sqrt(Math.pow(r - r, 2) + Math.pow(c - j, 2)) < 3){
                    ret-=0.025;
                }
            }
        }
        return ret;
    }

    /*
     * takes vector at index row as input and returns it on matrix format for matmultiplication
     * with T matrix.
     */
    private double[][] OVectToMat(int row){
        int vec_ind = 0;
        int count = 0;
        double[] obsvect = observationVectors[row];
        double[][] ret = new double[rows*4][cols*4];
        for (int i = 0; i < rows * cols * 4; i++) {
            for (int j = 0; j < rows * cols * 4; j++) {
                if(i == j){
                    ret[i][j] = obsvect[vec_ind];
                    count++;
                } else {
                    ret[i][j] = 0;
                }
                if(count >= 4){
                    vec_ind++;
                    count = 0;
                }
            }
        }
        return ret;
    }
    /*
     * returns the probability of finding the robot at r,c given the input reading rr, rc
     * cannot be used for outbounds calculations.
     */
    private double Oprob(int rr, int rc, int r, int c) {
        if (rr == r && rc == c) {
            return 0.1;
        } else if (Math.sqrt(Math.pow(rr - r, 2) + Math.pow(rc - c, 2)) < 2) {
            return 0.05;
        } else if (Math.sqrt(Math.pow(rr - r, 2) + Math.pow(rc - c, 2)) < 3) {
            return 0.025;
        } else {
            return 0;
        }
    }
    /*
     * returns the probability of transition from state <x, y, h> to <nX, nY, nH>.
     * Used for populating transitionMatrix.
     */
    private double Tprob( int x, int y, int h, int nX, int nY, int nH) {
        ArrayList<Integer> posDirs = possibleDirections(x, y);
        //move not valid --> 0 prob
        if (dirOfMove(x, y, nX, nY) != nH) {
            return 0;
        }

        //No walls nearby
        if (posDirs.size() == 4) {
            if (h == nH) {
                return 0.7;
            } else {
                return 0.1;
            }
        }
        //1 wall nearby
        else if (posDirs.size() == 3) {
            if (!posDirs.contains(h)) {
                if (dirOfMove(x, y, nX, nY) == nH) {
                    return 0.33;
                }
            } else {
                if (h == nH) {
                    return 0.7;
                } else {
                    return 0.15;
                }
            }
        }
        //corner
        else if (posDirs.size() == 2) {
            if (!posDirs.contains(h)) {
                if (dirOfMove(x, y, nX, nY) == nH) {
                    return 0.5;
                }
            } else {
                if (h == nH) {
                    return 0.7;
                } else {
                    return 0.3;
                }
            }
        }
        return 0;
    }

    /*
     * returns the direction of th input move and -1 if not possible move.
     */
    private int dirOfMove(int r, int c, int nr, int nc){
        if(r+1 == nr && c == nc){
            return SOUTH;
        }else if(r-1 == nr && c == nc){
            return NORTH;
        }else if(c+1 == nc && r == nr){
            return EAST;
        }else if(c-1 == nc && r == nr){
            return WEST;
        }
        return -1;
    }


    /*
     * returns the probability entry of the sensor matrices O to get reading r corresponding
     * to position (rX, rY) when actually in position (x, y) (note that you have to take
     * care of potentially necessary transformations from states i = <x, y, h> to
     * positions (x, y)).
     */
    public double getOrXY( int rX, int rY, int x, int y, int h) {
        return observationVectors[rX*cols + rY][x*cols + y];
    }

    @Override
    public double getTProb(int x, int y, int h, int nX, int nY, int nH) {
        return transitionMatrix[x*rows*head + y*head + h][nX*rows*head + nY*head + nH];
    }


    /*
     * returns the currently known true position i.e., after one simulation step
     * of the robot as (x,y)-pair.
     */
    public int[] getCurrentTrueState() {
        int[] ret = new int[3];
        ret[0] = row;
        ret[1] = col;
        ret[2] = currentHeading;
        return ret;
    }

    /*
     * returns the currently available sensor reading obtained for the true position
     * after the simulation step
     * returns null if the reading was "nothing" (whatever that stands for in your model)
     */
    public int[] getCurrentReading() {
        int[] ret = {0,0};
        int xoffset = 0;
        int yoffset = 0;
        Random rand = new Random();
        double randdouble = rand.nextDouble();

        if (randdouble < 0.1){
            int[] truestate = getCurrentTrueState();
            ret[0] = truestate[0];
            ret[1] = truestate[1];
        }
        else if (randdouble >= 0.1 && randdouble < 0.5) {
            int tilenr = rand.nextInt(offset1.length);

            xoffset = offset1[tilenr][0];
            yoffset = offset1[tilenr][1];
        }
        else if(randdouble >= 0.5 && randdouble < 0.9){
            int tilenr = rand.nextInt(offset2.length);

            xoffset = offset2[tilenr][0];
            yoffset = offset2[tilenr][1];
        }
        ret[0] = getCurrentTrueState()[0] + xoffset;
        ret[1] = getCurrentTrueState()[1] + yoffset;

        if(ret[0] < 0 || ret[0] >= cols || ret[1] < 0 || ret[1] >= rows){
            return null;
        }
        return ret;
    }

    /*
     * returns the currently estimated (summed) probability for the robot to be in position
     * (x,y) in the grid. The different headings are not considered, as it makes the
     * view somewhat unclear.
     */
    public double getCurrentProb(int x, int y) {
        double ret = 0.0;
        return ret;
    }

    /*
     * returns an array containing true/false depending on if the robot can move in INDEX direction.
     * NORTH = 0, EAST = 1, SOUTH = 2, WEST = 3
     */
    private ArrayList<Integer> possibleDirections(int r, int c){
        ArrayList<Integer> ret = new ArrayList<Integer>();
        if(r-1 >= 0){
            ret.add(NORTH);
        }
        if(c+1 < cols){
            ret.add(EAST);
        }
        if(r+1 < rows){
            ret.add(SOUTH);
        }
        if(c-1 >= 0){
            ret.add(WEST);
        }
        return ret;
    }

    /*
     * moves mr robot one step in the direction of head.
     */
    private void moveForward(){
        switch(currentHeading){
            case(NORTH):
                row -= 1;
                break;
            case(EAST):
                col += 1;
                break;
            case(SOUTH):
                row += 1;
                break;
            case(WEST):
                col -= 1;
                break;
        }
    }

    private void moveRobot(){
        ArrayList<Integer> posDirs = possibleDirections(row, col);

        if (posDirs.contains(currentHeading)) {
            if (Math.random() < 0.7) {
                moveForward();
            } else {
                Random r = new Random();
                posDirs.remove(currentHeading);
                currentHeading = posDirs.get(r.nextInt(posDirs.size()));
                moveForward();
            }
        } else {
            Random r = new Random();
            currentHeading = posDirs.get(r.nextInt(posDirs.size()));
            moveForward();
        }
    }

    private void printMat(double[][] mat, int xdim, int ydim){
        for(int i = 0; i < xdim; i++){
            for(int j = 0; j<ydim; j++){
                System.out.print(mat[i][j] + " ");
            }
            System.out.println();
        }
    }
    /*
     * should trigger one step of the estimation, i.e., true position, sensor reading and
     * the probability distribution for the position estimate should be updated one step
     * after the method has been called once.
     */
    public void update() {
        moveRobot();
    }
}