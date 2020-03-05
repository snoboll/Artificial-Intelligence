package model;

import control.EstimatorInterface;
import org.apache.commons.math3.distribution.EnumeratedIntegerDistribution;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

public class RobotLocalizer implements EstimatorInterface {

    private int rows, cols, head;
    private int x, y;
    private int rx, ry;
    private boolean sensor;

    private Filtering filterModel;

    // head = dir, 0 => up, 1 => right, 2 => down, 3 => left
    private int[] numsToGenerate = new int[]{ -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24};
    private double[] discreteProbabilities = new double[]{ 0.1, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.05, 0.05, 0.05, 0.025, 0.025, 0.05, 0.1, 0.05, 0.025, 0.025, 0.05, 0.05, 0.05, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025};
    private EnumeratedIntegerDistribution distribution = new EnumeratedIntegerDistribution(numsToGenerate, discreteProbabilities);

    private int[][] matrix = new int[][]{
        {-2,-2}, {-1,-2}, {0,-2}, {1,-2}, {2,-2},
        {-2,-1}, {-1,-1}, {0,-1}, {1,-1}, {2,-1},
        {-2,0}, {-1,0}, {0,0}, {1,0}, {2,0},
        {-2,1}, {-1,1}, {0,1}, {1,1}, {2,1},
        {-2,2}, {-1,2}, {0,2}, {1,2}, {2,2}};

    public RobotLocalizer( int rows, int cols, int head, int x, int y) {
        this.rows = rows;
        this.cols = cols;
        this.head = head;
        this.x = x;
        this.y = y;
        this.filterModel = new Filtering(rows, cols);
    }

    @Override
    public int getNumRows() {
        return this.rows;
    }

    @Override
    public int getNumCols() {
        return this.cols;
    }

    @Override
    public int getNumHead() {
        return this.head;
    }

    @Override
    public void update() {
        ArrayList<Integer> posibleDirs = getPosibleDirections(x, y);
        double rand = Math.random();
        if (!posibleDirs.contains(head)) {
            head = getRandomElement(posibleDirs);
            moveOneStep(head);
        }
        else if (rand <= 0.7){
            moveOneStep(head);
        }
        else {
            removeElement(head, posibleDirs);
            head = getRandomElement(posibleDirs);
            moveOneStep(head);
        }
        sensor = useSensor();
    }

    private void removeElement(int e, ArrayList<Integer> l){
        int index = 0;
        for (int i = 0; i < l.size(); i++){
            if (l.get(i) == e){
                index = i;
            }
        }
        l.remove(index);
    }

    private void moveOneStep(int dir){
        switch (dir) {
            case 0: y -= 1;
                break;
            case 1: x += 1;
                break;
            case 2: y += 1;
                break;
            case 3: x -= 1;
                break;
        }
    }

    private int getRandomElement(ArrayList<Integer> list)
    {
        Random rand = new Random();
        return list.get(rand.nextInt(list.size()));
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

    @Override
    public int[] getCurrentTrueState() {
        int[] ret = new int[3];
        ret[0] = y;
        ret[1] = x;
        ret[2] = head;
        return ret;
    }

    @Override
    public int[] getCurrentReading() {
        int[] ret = new int[3];
        if (sensor) {
            ret[0] = ry;
            ret[1] = rx;
            return ret;
        }
        else {
            return null;
        }
    }


    public boolean useSensor() {
        int reading = distribution.sample();
        int[] pos = getReturnPosFromInt(reading);
        if (pos != null){
            rx = pos[1];
            ry = pos[0];
            return true;
        }
        else {
            return false;
        }
    }

    @Override
    public double getCurrentProb(int x, int y) {
        ArrayList<Integer> sdirs = getPosibleDirections(rx, ry);
        double O = getOrXY(x,y,this.ry, this.rx, this.head);

        ArrayList<int[]> prevStates = getPrevStates(x, y);
        double T = 0;
        for (int[] point: prevStates) {
            T = T + getTProb(point[0], point[1], point[2], x, y, point[2]);
        }

        double ret = O * T;

        return ret;
    }

    private ArrayList<int[]> getPrevStates(int x, int y){
        ArrayList<int[]> prev = new ArrayList<>();
        // up
        int[] p = new int[]{x-1, y, 0};
        if (p[0] < 0){
            prev.add(p);
        }
        p = new int[]{x, y+1, 1};
        if (p[1] > rows-1){
            prev.add(p);
        }
        p = new int[]{x+1, y, 2};
        if (p[0] > rows-1){
            prev.add(p);
        }
        p = new int[]{x, y-1, 3};
        if (p[1] < 0){
            prev.add(p);
        }
        return prev;
    }

    @Override
    public double getOrXY(int rX, int rY, int x, int y, int h) {
        double distance = Math.sqrt(Math.pow(rX-x, 2) + Math.pow(rY-y, 2));
        if (distance == 0){
            return 0.1;
        }
        else if (distance < 2){
            return 0.05;
        }
        else if (distance < 3) {
            return 0.025;
        }
        return 0;
    }

    @Override
    public double getTProb(int x, int y, int h, int nX, int nY, int nH) {
        return filterModel.Tm[x+y+h][nX+nY+nH];
    }

    private int[] getReturnPosFromInt(int num) {
        int[] pos;
        if(num == -1){
            return null;
        }
        pos = matrix[num];
        pos = new int[]{y+pos[0], x+pos[1]};
        if (pos[0] < 0 || pos[1] < 0 || pos[0] > rows - 1 || pos[1] > cols - 1){
            return null;
        }
        return pos;
    }
}
