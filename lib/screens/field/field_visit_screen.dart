import 'package:flutter/material.dart';
import 'package:get/get.dart';

class FieldVisitScreen extends StatefulWidget {
  const FieldVisitScreen({super.key});

  @override
  State<FieldVisitScreen> createState() => _FieldVisitScreenState();
}

class _FieldVisitScreenState extends State<FieldVisitScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('FieldVisit'),
      ),
      body: Center(
        child: Text('FieldVisit - Coming Soon'),
      ),
    );
  }
}
