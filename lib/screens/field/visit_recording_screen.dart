import 'package:flutter/material.dart';
import 'package:get/get.dart';

class VisitRecordingScreen extends StatefulWidget {
  const VisitRecordingScreen({super.key});

  @override
  State<VisitRecordingScreen> createState() => _VisitRecordingScreenState();
}

class _VisitRecordingScreenState extends State<VisitRecordingScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('VisitRecording'),
      ),
      body: Center(
        child: Text('VisitRecording - Coming Soon'),
      ),
    );
  }
}
