import 'package:flutter/material.dart';
import 'package:get/get.dart';

class EmiCalculatorScreen extends StatefulWidget {
  const EmiCalculatorScreen({super.key});

  @override
  State<EmiCalculatorScreen> createState() => _EmiCalculatorScreenState();
}

class _EmiCalculatorScreenState extends State<EmiCalculatorScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('EmiCalculator'),
      ),
      body: Center(
        child: Text('EmiCalculator - Coming Soon'),
      ),
    );
  }
}
