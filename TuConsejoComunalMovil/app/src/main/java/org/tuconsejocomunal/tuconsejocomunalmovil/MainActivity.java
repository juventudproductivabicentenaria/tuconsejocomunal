package org.tuconsejocomunal.tuconsejocomunalmovil;

import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

import com.google.zxing.Result;

import me.dm7.barcodescanner.zxing.ZXingScannerView;

public class MainActivity extends AppCompatActivity implements ZXingScannerView.ResultHandler{
private ZXingScannerView escannerView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void EscannerQR(View view){

        escannerView=new ZXingScannerView(this);
        setContentView(escannerView);
        escannerView.setResultHandler(this);
        escannerView.startCamera();
    }

    @Override
    protected void onPause() {
        super.onPause();
        escannerView.stopCamera();
    }

    @Override
    public void handleResult(Result result) {

        AlertDialog.Builder builder=new AlertDialog.Builder(this);
        builder.setTitle("Resultado del Escanner");
        builder.setMessage(result.getText());
        AlertDialog alertDialog=builder.create();
        alertDialog.show();
        escannerView.resumeCameraPreview(this);


    }
}
