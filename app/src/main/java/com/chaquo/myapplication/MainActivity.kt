package com.chaquo.myapplication

import android.media.AudioManager
import android.media.MediaPlayer
import android.os.Bundle
import android.util.Log
import android.view.View.VISIBLE
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.PyException
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream

class MainActivity : AppCompatActivity() {

    lateinit var tempWav: File

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (! Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
        val py = Python.getInstance()
        val module = py.getModule("app")

        findViewById<Button>(R.id.button).setOnClickListener {
            try {
                Toast.makeText(this, "处理中...", Toast.LENGTH_LONG).show()
                val bytes = module.callAttr("vc_fn",
                                            findViewById<EditText>(R.id.etX).text.toString())
                    .toJava(ByteArray::class.java)
                tempWav = File.createTempFile("tmp", "wav", cacheDir)
                val fos = FileOutputStream(tempWav)
                fos.write(bytes)
                fos.close()
                Log.e("vits","success")
                findViewById<Button>(R.id.button2).visibility=VISIBLE
            } catch (e: PyException) {
                Toast.makeText(this, e.message, Toast.LENGTH_LONG).show()
                Log.e("PyException",e.toString())
            }
        }
        findViewById<Button>(R.id.button2).setOnClickListener {
            val fis = FileInputStream(tempWav)
            MediaPlayer().apply {
                setAudioStreamType(AudioManager.STREAM_MUSIC)
                setDataSource(fis.fd)
                prepare()
                start()
            }
            fis.close()
        }
    }

}