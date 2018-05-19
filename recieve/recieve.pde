import org.gwoptics.graphics.graph2D.Graph2D;
import org.gwoptics.graphics.graph2D.traces.*;
import org.gwoptics.graphics.graph2D.backgrounds.*;
import org.gwoptics.graphics.GWColour;
import processing.serial.*;
import java.lang.Math.*;
import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;

PFont font;

boolean serial = true;          // set to true to use Serial, false to use OSC messages.

String serialPort = "/dev/cu.usbserial-A5056WMY";      // change this to your COM port 

/////////////////////////////////////////////////////////////
//////////////////////  variables ///////////////////////////
/////////////////////////////////////////////////////////////
PrintWriter file;

PrintWriter summary;

boolean testing; 

Serial myPort;

Graph[] power_graphs = new Graph[5];

Graph[] sus_graphs = new Graph[4];

Graph temp;

///SHUTDOWN BUTTON
int shutdownX = 0;
int shutdownY = 675;
int shutdownH = 125;
int shutdownW = 500;

int     lf = 10;       //ASCII linefeed
String  inString;      //String for testing serial communication
int[] rgb_color = {0, 0, 255, 0, 160, 122, 0, 255, 0, 255};

String calib_status = "";

int powerMax = 500;

int powerMin = 200;

int susMax = 500;

int susMin = 200;

int tempMax = 200;

int tempMin = 50;


int dataPoints = 0;

Date start;

Event hottest;
Event coolest; 
double avgTemp = 0;

Event powerH;
Event powerL; 
double powerAvg = 0;

/////////////////////////////////////////////////////////////
///////// class needed for the timeseries graph /////////////
/////////////////////////////////////////////////////////////

class rangeData implements ILine2DEquation{
    private double curVal = 0;

    public void setCurVal(double curVal) {
      this.curVal = curVal;      
    }
    
    public double getCurVal() {
      return this.curVal;
    }
    
    public double computePoint(double x,int pos) {
      return curVal;
    }
}

class Graph {
  public Graph2D chart;
  public ArrayList<rangeData> data;
  
  Graph(Graph2D chart, ArrayList<rangeData> data) {
    this.chart = chart;
    this.data = data;
  }
}

void setup(){
  this.testing = false;
  font = createFont("font.otf", 34);
  DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH-mm-ss");
  start = new Date();
  file = createWriter("tests/" + dateFormat.format(start) + "/data.txt"); 
  summary = createWriter("tests/" + dateFormat.format(start) + "/summary.txt");
  summary.println("Test: " + new SimpleDateFormat("yyyy/MM/dd' T 'HH:mm:ss").format(new Date()));
  size(1100,800, P3D);
  surface.setResizable(true);
  stroke(0,0,0);
  colorMode(RGB, 256); 
 

  if(serial){
    try{
      printArray(Serial.list());
      // Open the port you are using at the rate you want:
      myPort = new Serial(this, serialPort, 9600);
      myPort.clear();
      //myPort.bufferUntil(lf);
    }catch(Exception e){
      println("Cannot open serial port.");
      print(e);
    }
  }
  
  for(int ii=0; ii < power_graphs.length; ii++)
  {
    power_graphs[ii] = new Graph(new Graph2D(this, 400, 75, false), new ArrayList<rangeData>());
  }
  
  for(int ii=0; ii < sus_graphs.length; ii++)
  {
    sus_graphs[ii] = new Graph(new Graph2D(this, 400, 75, false), new ArrayList<rangeData>());
  }
  
  temp = new Graph(new Graph2D(this, 400, 75, false), new ArrayList<rangeData>());
  
  int ii = 0;
  for(Graph g: power_graphs){
    rangeData r = new rangeData();
    g.data.add(r);
    RollingLine2DTrace rl = new RollingLine2DTrace(r ,100,0.1f);
    rl.setTraceColour(rgb_color[6], rgb_color[7], rgb_color[8]);
    rl.setLineWidth(2);
    g.chart.addTrace(rl);
    g.chart.setYAxisMin(powerMin);
    g.chart.setYAxisMax(powerMax);
    g.chart.position.y = 130*ii+10;
    g.chart.position.x = 75;    
    g.chart.setYAxisTickSpacing((powerMax-powerMin)/5);
    g.chart.setXAxisTickSpacing(2f);
    g.chart.setXAxisMax(15f);
    g.chart.setXAxisMin(0f);
    g.chart.setFontColour(255, 255, 255);
    g.chart.setXAxisLabel("Time (s)");
    g.chart.setYAxisLabel("Power " + (1 + ii));
    g.chart.setBackground(new SolidColourBackground(new GWColour(1f, 1f, 1f)));
    ii ++;
  }
  ii = 0;
    for(Graph g: sus_graphs){
    rangeData r = new rangeData();
    g.data.add(r);
    RollingLine2DTrace rl = new RollingLine2DTrace(r, 100, 0.1f);
    rl.setTraceColour(rgb_color[6], rgb_color[7], rgb_color[8]);
    rl.setLineWidth(2);
    g.chart.addTrace(rl);
    g.chart.setYAxisMin(susMin);
    g.chart.setYAxisMax(susMax);
    g.chart.position.y = 130 * ii + 10;
    g.chart.position.x = 600;    
    g.chart.setYAxisTickSpacing((susMax-susMin)/5);
    g.chart.setXAxisTickSpacing(2f);
    g.chart.setXAxisMax(15f);
    g.chart.setXAxisMin(0f);
    g.chart.setFontColour(255, 255, 255);
    g.chart.setXAxisLabel("Time (s)");
    g.chart.setYAxisLabel("Suspension " + (1 + ii));
    g.chart.setBackground(new SolidColourBackground(new GWColour(1f, 1f, 1f)));
    ii ++;
  }
  
    rangeData r = new rangeData();
    temp.data.add(r);
    RollingLine2DTrace rl = new RollingLine2DTrace(r, 100, 0.1f);
    rl.setTraceColour(rgb_color[6], rgb_color[7], rgb_color[8]);
    rl.setLineWidth(2);
    temp.chart.addTrace(rl);
    temp.chart.setYAxisMin(tempMin);
    temp.chart.setYAxisMax(tempMax);
    temp.chart.position.y = 600;
    temp.chart.position.x = 600;    
    temp.chart.setYAxisTickSpacing((tempMax-tempMin)/5);
    temp.chart.setXAxisTickSpacing(2f);
    temp.chart.setXAxisMax(15f);
    temp.chart.setXAxisMin(0f);
    temp.chart.setFontColour(255, 255, 255);
    temp.chart.setXAxisLabel("Time (s)");
    temp.chart.setYAxisLabel("Temperature (C)");
    temp.chart.setBackground(new SolidColourBackground(new GWColour(1f, 1f, 1f)));
}

void draw(){
    background(0, 0, 0);
    // show some text
    fill(100,100,100);
    textFont(font);
    text("PROVE", 740, 770);
    fill(0, 0, 0);
    // draw the graphs
    for(Graph g: power_graphs) {
      g.chart.draw();
    }
    
    for(Graph g: sus_graphs) {
      g.chart.draw();
    }
    
    temp.chart.draw();
    if(mouseX > shutdownX && mouseX < (shutdownX + shutdownW) && mouseY > shutdownY && mouseY < (shutdownY + shutdownH)) {
      fill(220,20,60); 
    } else{
      fill(255,255,255);
    }
    rect(shutdownX, shutdownY, shutdownW, shutdownH);
    fill(0,0,0);
    text(this.testing ? "STOP" : "START", 120, 750);
}

void mouseClicked() {
  if(mouseX > shutdownX && mouseX < (shutdownX + shutdownW) && mouseY > shutdownY && mouseY < (shutdownY + shutdownH)) {
      EMGSTOP();
      myPort.write(22);
  } 
}
 
void serialEvent(Serial myPort) {
  inString = (myPort.readString());
  file.close();
  println(inString);
  try {
    //Parse the data
    String[] dataStrings = split(inString, ',');
    if (dataStrings.length == 10) {
      dataPoints ++;
      int index = 0;
      for(Graph g: power_graphs) {
        g.data.get(0).setCurVal(float(dataStrings[index]));
        index++;
      }
      
      index = 0;
      for(Graph g: sus_graphs) {
        g.data.get(0).setCurVal(float(dataStrings[index + power_graphs.length]));
        index++;
      }
      
      temp.data.get(0).setCurVal(float(dataStrings[index]));
      avgTemp += float(dataStrings[index]);
      if(coolest == null || coolest.getData() > float(dataStrings[index]))
        coolest.setData(float(dataStrings[index]));
      if(hottest == null || hottest.getData() < float(dataStrings[index]))
        hottest.setData(float(dataStrings[index]));
    }
  } catch (Exception e) {
      println("Error while reading serial data. " + e);
  }
}

void EMGSTOP() {
   //println("EMG STOP");
   //summary.println("EMG STOP AT " + new SimpleDateFormat("HH:mm:ss").format(new Date()));
   this.testing = !this.testing;
}

void exit() {
  print("Exiting");
  file.flush();
  file.close();
  summary.println(coolest != null? coolest.getEvent() : null);
  summary.println(hottest != null ? hottest.getEvent() : null);
  summary.println("Average temperature: " + avgTemp / dataPoints);
  summary.println("Test stopped at " + new SimpleDateFormat("HH:mm:ss").format(new Date()));
  summary.println("Test duration: " + -.001 * (start.getTime() - new Date().getTime()) + " seconds");
  summary.flush();
  summary.close();
  super.exit();
}

interface Event {
   String getEvent();
   float getData();
   void setData(float data);
}

class tempEvent implements Event{
   private float data;
   private Date date;
   
   public void setData(float data) {
     this.data = data;
   }
   
   public float getData() {
     return this.data;
   }
   
   tempEvent(Float data) {
      this.data = data;
      this.date = new Date();
   }
   
   public String getEvent() {
      return "Reached " + this.data + " at " + new SimpleDateFormat("HH:mm:ss").format(this.date); 
   }
}