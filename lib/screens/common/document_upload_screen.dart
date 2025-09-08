import 'package:flutter/material.dart';
import 'package:get/get.dart';

class DocumentUploadScreen extends StatefulWidget {
  const DocumentUploadScreen({super.key});

  @override
  State<DocumentUploadScreen> createState() => _DocumentUploadScreenState();
}

class _DocumentUploadScreenState extends State<DocumentUploadScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('DocumentUpload'),
      ),
      body: Center(
        child: Text('DocumentUpload - Coming Soon'),
      ),
    );
  }
}
