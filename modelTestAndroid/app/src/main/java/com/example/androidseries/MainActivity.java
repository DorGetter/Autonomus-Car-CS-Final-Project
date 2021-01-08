package com.example.androidseries;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.os.Bundle;
import android.os.Environment;
import android.util.Pair;
import android.view.SurfaceView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfRect;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.tensorflow.lite.Interpreter;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;

import static org.opencv.core.CvType.CV_32F;

//import com.chaquo.python.PyObject;
//import com.chaquo.python.Python;
//import com.chaquo.python.android.AndroidPlatform;



public class MainActivity extends AppCompatActivity implements CameraBridgeViewBase.CvCameraViewListener2 {

    CameraBridgeViewBase    cameraBridgeViewBase ;
    BaseLoaderCallback      baseLoaderCallback;  // allows as to get the frames from the camera

    Button btn;
    ImageView iv;
    BitmapDrawable drawable;
    Bitmap bitmap;
    String imageString = "";
    Interpreter interperter;
    CascadeClassifier detector;
    CascadeClassifier detectorPed;
    File cascadeFileCarDet;
    File cascadeFilePedestrain;
    int counterFrme= 0 ;
    float steering_angle_ ;

    TextView steering;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

//        steering = (TextView) findViewById(R.id.steering_angle);

//        if(steering_angle_< 0 )
//            steering.setText("turn left" + steering_angle_ * -1 + "% of the wheel");
//
//        if(steering_angle_ > 0 )
//            steering.setText("turn right" + steering_angle_  + "% of the wheel");
        cameraBridgeViewBase = (JavaCameraView) findViewById(R.id.CameraView);
        cameraBridgeViewBase.setVisibility(SurfaceView.VISIBLE);
        cameraBridgeViewBase.setCvCameraViewListener(this);

        baseLoaderCallback = new BaseLoaderCallback(this) {
            @Override
            public void onManagerConnected(int status) {
                super.onManagerConnected(status);
                switch (status){
                    case BaseLoaderCallback.SUCCESS:
                        cameraBridgeViewBase.enableView();
                        initFileCascadeCarsDet();
                        initFileCascadePedestrains();
                        break;
                    default:
                        super.onManagerConnected(status);
                        break;
                }
            }
        };


        try {
            interperter = new Interpreter(loadModelFile(), null);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void initFileCascadePedestrains() {
        try {
            System.out.println("init file Cascade");

            InputStream is = getResources().openRawResource(R.raw.pedestrian);
            File cascadeDir = getDir("cascade", Context.MODE_PRIVATE);
            cascadeFilePedestrain = new File(cascadeDir, "pedestrian.xml");

            FileOutputStream os = new FileOutputStream(cascadeFilePedestrain);
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = is.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
            is.close();
            os.close();
            detectorPed = new CascadeClassifier(cascadeFilePedestrain.getAbsolutePath());

            if(detectorPed.empty()){
                detectorPed = null;
            }
            else{
                cascadeDir.delete();
            }
        } catch (Exception e) {
            System.out.println("something wrong!");
            e.printStackTrace();
        }
    }




    private void initFileCascadeCarsDet() {
        try {
            System.out.println("init file Cascade");

            InputStream is = getResources().openRawResource(R.raw.cars_detect);
            File cascadeDir = getDir("cascade", Context.MODE_PRIVATE);
            cascadeFileCarDet = new File(cascadeDir, "cars_detect.xml");

            FileOutputStream os = new FileOutputStream(cascadeFileCarDet);
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = is.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
            is.close();
            os.close();
            detector = new CascadeClassifier(cascadeFileCarDet.getAbsolutePath());

            if(detector.empty()){
                detector = null;
            }
            else{
                cascadeDir.delete();
            }
        } catch (Exception e) {
            System.out.println("something wrong!");
            e.printStackTrace();
        }
    }

    // this is the important one...
    // getting frames from camera before showing it.
    // here need to implement the logic's. processing media
    // Mat is the metrics of the frame. 20/30 fps
    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
//        steering = (TextView) findViewById(R.id.steering_angle);


        Mat frame = inputFrame.rgba();
        steering_angle_ = get_steering_prediction(frame.clone());
        Mat displayMat = null;
//        if(counterFrme % 10  == 0 || counterFrme %10 ==1 || counterFrme %10 ==2 || counterFrme %10 ==3 || counterFrme %10 ==4   ) {
            displayMat  = draw_LaneLines(frame.clone());
//            displayMat = CarDetect(displayMat);
//            displayMat = PedestrainDet(frame.clone());

//        }else{
//            displayMat = frame;
//        }

        counterFrme ++;
        if(steering_angle_< 0 ) {
            Imgproc.putText(
                    displayMat,                          // Matrix obj of the image
                    "turn left " + steering_angle_ * -1 + "% of the wheel",          // Text to be added
                    new Point(10, 50),               // point
                    Core.FONT_HERSHEY_SIMPLEX,      // front face
                    1,                               // front scale
                    new Scalar(255, 0, 0),             // Scalar object for color
                    6                                // Thickness
            );
        }
        if(steering_angle_ > 0 ) {
            Imgproc.putText(
                    displayMat,                          // Matrix obj of the image
                    "turn right " + steering_angle_  + "% of the wheel",          // Text to be added
                    new Point(10, 50),               // point
                    Core.FONT_HERSHEY_SIMPLEX,      // front face
                    1,                               // front scale
                    new Scalar(255, 0, 0),             // Scalar object for color
                    6                                // Thickness
            );
        }

        return displayMat;

    }

    private Mat PedestrainDet(Mat frame_clone) {
        MatOfRect mRect = new MatOfRect();

        detector.detectMultiScale(frame_clone, mRect);

        for ( Rect rect : mRect.toArray()){
            Imgproc.rectangle(frame_clone, new Point(rect.x, rect.y),
                    new Point(rect.x + rect.width,rect.y+rect.height),
                    new Scalar(255,0,0));
        }

        return frame_clone;

    }

    private Mat CarDetect(Mat frame_clone){
        MatOfRect mRect = new MatOfRect();

        detector.detectMultiScale(frame_clone, mRect);

        for ( Rect rect : mRect.toArray()){
            Imgproc.rectangle(frame_clone, new Point(rect.x, rect.y),
                    new Point(rect.x + rect.width,rect.y+rect.height),
                    new Scalar(255,0,0));
        }

        return frame_clone;

    }


    private Mat draw_LaneLines(Mat frame){
        Mat gray = frame.clone();
        Imgproc.cvtColor(gray, gray, Imgproc.COLOR_RGBA2GRAY);
        Imgproc.GaussianBlur(gray,gray,new Size(5,5),0,0);
        Imgproc.Canny(gray,gray,60,140);

        int height = gray.rows();
        int width = gray.cols();
        System.out.println("hei "+ height + "wid " + width);
        Mat mask = new Mat(height,width, CvType.CV_8UC1,Scalar.all(0));
        Point[] rook_points = new Point[3];
        rook_points[0]  = new Point(200,height);
        rook_points[1]  = new Point(width/2 +50, height/2);
        rook_points[2]  = new Point(width-50,height);
        MatOfPoint matPt = new MatOfPoint();
        matPt.fromArray(rook_points);

        List<MatOfPoint> ppt = new ArrayList<MatOfPoint>();
        ppt.add(matPt);
        Imgproc.fillPoly(mask,
                ppt,
                new Scalar( 255,255,255 )
        );

        Mat after_bit = new Mat();
        Core.bitwise_and(gray,mask,after_bit);
//        lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
        Mat result = after_bit.clone();
        Mat lines = new Mat();
        Imgproc.HoughLinesP(after_bit, lines, 2, Math.PI/180, 100, 50, 4);

        Mat frame_clone = frame.clone();

        ArrayList<Pair<Double, Double>> left_fit = new ArrayList<>();
        ArrayList<Pair<Double, Double>> right_fit = new ArrayList<>();

        double left_slope_avr = 0;
        double right_slope_avr = 0;
        double left_iterccept_avr = 0;
        double right_iterccept_avr = 0;
        ///going through lines:
        for(int j = 0; j < lines.rows(); j++) {
            for (int i = 0; i < lines.cols(); i++) {
                double[] val = lines.get(j, i);
                double x1 = val[0];                double y1 = val[1];
                double x2 = val[2];                double y2 = val[3];
                double slope = Double.MAX_VALUE;
                double intercept = 0;
                boolean flag_slope_inter =false;

                if(x1-x2!=0 ) {
                    slope = (y1 - y2) / (x1 - x2);
                    intercept = (y1 - (slope*x1)) ;
                    flag_slope_inter = true;
                }

                if ( slope < 0  && flag_slope_inter) {
                    left_fit.add(new Pair(slope, intercept));
                    left_slope_avr += slope;
                    left_iterccept_avr += intercept;
                }
                else if ( slope > 0 && flag_slope_inter) {
                    right_fit.add(new Pair(slope, intercept));
                    right_slope_avr += slope;
                    right_iterccept_avr += intercept;
                }
                // y = slope * x + b
//                System.out.println("[x1: " + val[0] + " y1: " + val[1] + "x2: " + val[2] + "y2: " + val[3] + " ]");
//                Imgproc.line(result, new Point(val[0], val[1]), new Point(val[2], val[3]), new Scalar(0, 0, 255), 2);
            }

        }

        left_slope_avr = left_slope_avr/left_fit.size();
        left_iterccept_avr = left_iterccept_avr/left_fit.size();
        right_slope_avr = right_slope_avr/right_fit.size();
        right_iterccept_avr = right_iterccept_avr/right_fit.size();

        int [] points_Left_line = make_points(left_slope_avr, left_iterccept_avr, height);
        int [] points_Right_line = make_points(right_slope_avr, right_iterccept_avr, height);

        Imgproc.line(frame_clone, new Point(points_Left_line[0], points_Left_line[1]), new Point(points_Left_line[2], points_Left_line[3]), new Scalar(255, 0, 0), 10);
        Imgproc.line(frame_clone, new Point(points_Right_line[0], points_Right_line[1]), new Point(points_Right_line[2], points_Right_line[3]), new Scalar(255, 0, 0), 10);
        return frame_clone;
//    return mask;
    }

    private int[] make_points(double slope, double intercept, int height) {
        int [] ret = new int[4];
        int y1 = height;
        int y2 = y1*3/5;
        int x1 = (int)((y1-intercept)/slope);
        int x2 = (int)((y2-intercept)/slope);
        ret[0] = x1 ;
        ret[1] = y1 ;
        ret[2] = x2 ;
        ret[3] = y2 ;
        return ret;
    }

    /**
     * getting car steering prediction using keras model.
     * @param frame camera frame
     * @return -1 to 1 float
     */
    private float get_steering_prediction(Mat frame){
        Imgproc.cvtColor(frame, frame, Imgproc.COLOR_RGBA2RGB);
        Imgproc.cvtColor(frame, frame, Imgproc.COLOR_RGB2YUV);
        Imgproc.GaussianBlur(frame, frame, new Size(3, 3), 0, 0);

        Mat f = new Mat();
        Imgproc.resize(frame,f,new Size(200, 66));
        //   f = Dnn.blobFromImage(f, 0.00392, new Size(200, 66) , new Scalar(0,0 ,0), false,false);
        f.convertTo(f,CV_32F);
        StringBuilder sb = new StringBuilder();
        String s = new String();
        System.out.println("hei "+ f.height()+", wit" + f.width() + "ch " + f.channels());
        System.out.println("col "+ f.cols()+", row" + f.rows() + "ch " + f.channels());

        float[][][][] inputs = new float[1][200][66][3];
        float fs[] = new float[3];
        for( int r=0 ; r<f.rows() ; r++ ) {
            //sb.append(""+r+") ");
            for( int c=0 ; c<f.cols() ; c++ ) {
                f.get(r, c, fs);
                //sb.append( "{");
                inputs[0][c][r][0]=fs[0]/255;
                inputs[0][c][r][1]=fs[1]/255;
                inputs[0][c][r][2]=fs[2]/255;
                //sb.append( String.valueOf(fs[0]));
                //sb.append( ' ' );
                //sb.append( String.valueOf(fs[1]));
                //sb.append( ' ' );
                //sb.append( String.valueOf(fs[2]));
                //sb.append( "}");
                //sb.append( ' ' );
            }
            //sb.append( '\n' );
        }
        //System.out.println(sb);




        float[][] outputs = new float[1][1];
        interperter.run(inputs ,outputs);
        System.out.println("output: " + outputs[0][0]);
        return outputs[0][0];
    }

    private MappedByteBuffer loadModelFile() throws IOException{
        AssetFileDescriptor assetFileDescriptor = this.getAssets().openFd("model.tflite");
        FileInputStream fileInputStream = new FileInputStream(assetFileDescriptor.getFileDescriptor());
        FileChannel fileChannel = fileInputStream.getChannel();
        long startoffset = assetFileDescriptor.getStartOffset();
        long length = assetFileDescriptor.getLength();

        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startoffset, length);
    }

    @Override
    public void onCameraViewStarted(int width, int height) {

    }

    @Override
    public void onCameraViewStopped() {

    }

    @Override
    protected void onResume() {
        super.onResume();
        if(!OpenCVLoader.initDebug()){
            Toast.makeText(getApplicationContext(), "there's a problem!", Toast.LENGTH_LONG).show();
        }else{
            baseLoaderCallback.onManagerConnected(baseLoaderCallback.SUCCESS);
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        if(cameraBridgeViewBase!=null){
            cameraBridgeViewBase.disableView();
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if(cameraBridgeViewBase!=null){
            cameraBridgeViewBase.disableView();
        }
    }
}