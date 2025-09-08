import 'package:flutter/material.dart';
import 'package:get/get.dart';

class FieldScheduleScreen extends StatefulWidget {
  const FieldScheduleScreen({super.key});

  @override
  State<FieldScheduleScreen> createState() => _FieldScheduleScreenState();
}

class _FieldScheduleScreenState extends State<FieldScheduleScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('FieldSchedule'),
      ),
      body: Center(
        child: Text('FieldSchedule - Coming Soon'),
      ),
    );
  }
}
