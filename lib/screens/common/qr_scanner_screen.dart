import 'package:flutter/material.dart';
import 'package:get/get.dart';

class QrScannerScreen extends StatefulWidget {
  const QrScannerScreen({super.key});

  @override
  State<QrScannerScreen> createState() => _QrScannerScreenState();
}

class _QrScannerScreenState extends State<QrScannerScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('QrScanner'),
      ),
      body: Center(
        child: Text('QrScanner - Coming Soon'),
      ),
    );
  }
}
