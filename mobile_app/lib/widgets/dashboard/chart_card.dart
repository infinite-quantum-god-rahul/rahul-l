import 'package:flutter/material.dart';
import '../../config/app_theme.dart';

class ChartCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final String chartType;
  final List<Map<String, dynamic>> data;
  final Color color;
  final VoidCallback? onTap;
  final bool isLoading;
  final String? errorMessage;

  const ChartCard({
    Key? key,
    required this.title,
    required this.subtitle,
    required this.chartType,
    required this.data,
    required this.color,
    this.onTap,
    this.isLoading = false,
    this.errorMessage,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: color.withOpacity(0.1),
            blurRadius: 20,
            offset: const Offset(0, 8),
          ),
        ],
        border: Border.all(
          color: color.withOpacity(0.2),
          width: 1,
        ),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: AppTheme.lightTheme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w600,
                          color: AppTheme.textPrimaryColor,
                        ),
                      ),
                      Text(
                        subtitle,
                        style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                          color: AppTheme.textSecondaryColor,
                        ),
                      ),
                    ],
                  ),
                ),
                if (onTap != null)
                  Icon(
                    Icons.chevron_right,
                    color: AppTheme.textSecondaryColor.withOpacity(0.5),
                    size: 20,
                  ),
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Chart Content
            if (isLoading)
              _buildLoadingState()
            else if (errorMessage != null)
              _buildErrorState()
            else
              _buildChart(),
          ],
        ),
      ),
    );
  }

  Widget _buildLoadingState() {
    return Container(
      height: 120,
      width: double.infinity,
      decoration: BoxDecoration(
        color: AppTheme.textSecondaryColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
      ),
      child: const Center(
        child: CircularProgressIndicator(),
      ),
    );
  }

  Widget _buildErrorState() {
    return Container(
      height: 120,
      width: double.infinity,
      decoration: BoxDecoration(
        color: AppTheme.errorColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: AppTheme.errorColor.withOpacity(0.3),
        ),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              color: AppTheme.errorColor,
              size: 24,
            ),
            const SizedBox(height: 8),
            Text(
              errorMessage!,
              style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                color: AppTheme.errorColor,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChart() {
    switch (chartType.toLowerCase()) {
      case 'line':
        return _buildLineChart();
      case 'bar':
        return _buildBarChart();
      case 'pie':
        return _buildPieChart();
      case 'area':
        return _buildAreaChart();
      case 'doughnut':
        return _buildDoughnutChart();
      default:
        return _buildSimpleChart();
    }
  }

  Widget _buildLineChart() {
    return Container(
      height: 120,
      width: double.infinity,
      child: CustomPaint(
        painter: LineChartPainter(
          data: data,
          color: color,
        ),
      ),
    );
  }

  Widget _buildBarChart() {
    return Container(
      height: 120,
      width: double.infinity,
      child: CustomPaint(
        painter: BarChartPainter(
          data: data,
          color: color,
        ),
      ),
    );
  }

  Widget _buildPieChart() {
    return Container(
      height: 120,
      width: double.infinity,
      child: CustomPaint(
        painter: PieChartPainter(
          data: data,
          color: color,
        ),
      ),
    );
  }

  Widget _buildAreaChart() {
    return Container(
      height: 120,
      width: double.infinity,
      child: CustomPaint(
        painter: AreaChartPainter(
          data: data,
          color: color,
        ),
      ),
    );
  }

  Widget _buildDoughnutChart() {
    return Container(
      height: 120,
      width: double.infinity,
      child: CustomPaint(
        painter: DoughnutChartPainter(
          data: data,
          color: color,
        ),
      ),
    );
  }

  Widget _buildSimpleChart() {
    return Container(
      height: 120,
      width: double.infinity,
      child: CustomPaint(
        painter: SimpleChartPainter(
          data: data,
          color: color,
        ),
      ),
    );
  }
}

// Custom painters for different chart types
class LineChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> data;
  final Color color;

  LineChartPainter({required this.data, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    if (data.isEmpty) return;

    final paint = Paint()
      ..color = color
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    final fillPaint = Paint()
      ..color = color.withOpacity(0.1)
      ..style = PaintingStyle.fill;

    final path = Path();
    final fillPath = Path();
    
    final maxValue = data.map((e) => e['value'] as num).reduce((a, b) => a > b ? a : b);
    final minValue = data.map((e) => e['value'] as num).reduce((a, b) => a < b ? a : b);
    final valueRange = maxValue - minValue;

    for (int i = 0; i < data.length; i++) {
      final x = (i / (data.length - 1)) * size.width;
      final normalizedValue = valueRange == 0 ? 0.5 : (data[i]['value'] - minValue) / valueRange;
      final y = size.height - (normalizedValue * size.height);

      if (i == 0) {
        path.moveTo(x, y);
        fillPath.moveTo(x, size.height);
        fillPath.lineTo(x, y);
      } else {
        path.lineTo(x, y);
        fillPath.lineTo(x, y);
      }
    }

    // Close the fill path
    fillPath.lineTo(size.width, size.height);
    fillPath.close();

    // Draw fill first
    canvas.drawPath(fillPath, fillPaint);
    
    // Draw line on top
    canvas.drawPath(path, paint);

    // Draw data points
    final pointPaint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    for (int i = 0; i < data.length; i++) {
      final x = (i / (data.length - 1)) * size.width;
      final normalizedValue = valueRange == 0 ? 0.5 : (data[i]['value'] - minValue) / valueRange;
      final y = size.height - (normalizedValue * size.height);

      canvas.drawCircle(Offset(x, y), 3, pointPaint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class BarChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> data;
  final Color color;

  BarChartPainter({required this.data, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    if (data.isEmpty) return;

    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    final maxValue = data.map((e) => e['value'] as num).reduce((a, b) => a > b ? a : b);
    final barWidth = size.width / data.length * 0.8;
    final spacing = size.width / data.length * 0.2;

    for (int i = 0; i < data.length; i++) {
      final x = i * (barWidth + spacing);
      final normalizedValue = maxValue == 0 ? 0 : data[i]['value'] / maxValue;
      final barHeight = normalizedValue * size.height;

      final rect = Rect.fromLTWH(x, size.height - barHeight, barWidth, barHeight);
      
      // Create gradient effect
      final gradient = LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [
          color.withOpacity(0.8),
          color,
        ],
      );
      
      final gradientPaint = Paint()
        ..shader = gradient.createShader(rect);

      canvas.drawRect(rect, gradientPaint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class PieChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> data;
  final Color color;

  PieChartPainter({required this.data, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    if (data.isEmpty) return;

    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width < size.height ? size.width / 3 : size.height / 3;
    
    final total = data.map((e) => e['value'] as num).reduce((a, b) => a + b);
    double startAngle = 0;

    for (int i = 0; i < data.length; i++) {
      final value = data[i]['value'] as num;
      final sweepAngle = (value / total) * 2 * 3.14159;
      
      final paint = Paint()
        ..color = _getColorForIndex(i)
        ..style = PaintingStyle.fill;

      final rect = Rect.fromCircle(center: center, radius: radius);
      canvas.drawArc(rect, startAngle, sweepAngle, true, paint);
      
      startAngle += sweepAngle;
    }
  }

  Color _getColorForIndex(int index) {
    final colors = [
      color,
      color.withOpacity(0.8),
      color.withOpacity(0.6),
      color.withOpacity(0.4),
      color.withOpacity(0.2),
    ];
    return colors[index % colors.length];
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class AreaChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> data;
  final Color color;

  AreaChartPainter({required this.data, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    if (data.isEmpty) return;

    final paint = Paint()
      ..color = color.withOpacity(0.3)
      ..style = PaintingStyle.fill;

    final path = Path();
    
    final maxValue = data.map((e) => e['value'] as num).reduce((a, b) => a > b ? a : b);
    final minValue = data.map((e) => e['value'] as num).reduce((a, b) => a < b ? a : b);
    final valueRange = maxValue - minValue;

    // Start from bottom left
    path.moveTo(0, size.height);

    for (int i = 0; i < data.length; i++) {
      final x = (i / (data.length - 1)) * size.width;
      final normalizedValue = valueRange == 0 ? 0.5 : (data[i]['value'] - minValue) / valueRange;
      final y = size.height - (normalizedValue * size.height);

      path.lineTo(x, y);
    }

    // Close the path to bottom right
    path.lineTo(size.width, size.height);
    path.close();

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class DoughnutChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> data;
  final Color color;

  DoughnutChartPainter({required this.data, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    if (data.isEmpty) return;

    final center = Offset(size.width / 2, size.height / 2);
    final outerRadius = size.width < size.height ? size.width / 3 : size.height / 3;
    final innerRadius = outerRadius * 0.6;
    
    final total = data.map((e) => e['value'] as num).reduce((a, b) => a + b);
    double startAngle = 0;

    for (int i = 0; i < data.length; i++) {
      final value = data[i]['value'] as num;
      final sweepAngle = (value / total) * 2 * 3.14159;
      
      final paint = Paint()
        ..color = _getColorForIndex(i)
        ..style = PaintingStyle.fill;

      // Draw outer arc
      final outerRect = Rect.fromCircle(center: center, radius: outerRadius);
      canvas.drawArc(outerRect, startAngle, sweepAngle, true, paint);
      
      // Cut out inner circle
      final innerRect = Rect.fromCircle(center: center, radius: innerRadius);
      final cutoutPaint = Paint()
        ..color = Colors.white
        ..style = PaintingStyle.fill;
      canvas.drawArc(innerRect, startAngle, sweepAngle, true, cutoutPaint);
      
      startAngle += sweepAngle;
    }
  }

  Color _getColorForIndex(int index) {
    final colors = [
      color,
      color.withOpacity(0.8),
      color.withOpacity(0.6),
      color.withOpacity(0.4),
      color.withOpacity(0.2),
    ];
    return colors[index % colors.length];
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class SimpleChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> data;
  final Color color;

  SimpleChartPainter({required this.data, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    if (data.isEmpty) return;

    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width < size.height ? size.width / 4 : size.height / 4;

    // Draw a simple circle
    canvas.drawCircle(center, radius, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

// Specialized chart card variants
class ChartCardWithLegend extends StatelessWidget {
  final String title;
  final String subtitle;
  final String chartType;
  final List<Map<String, dynamic>> data;
  final Color color;
  final VoidCallback? onTap;
  final bool showLegend;
  final List<Color>? legendColors;

  const ChartCardWithLegend({
    Key? key,
    required this.title,
    required this.subtitle,
    required this.chartType,
    required this.data,
    required this.color,
    this.onTap,
    this.showLegend = true,
    this.legendColors,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: color.withOpacity(0.1),
            blurRadius: 20,
            offset: const Offset(0, 8),
          ),
        ],
        border: Border.all(
          color: color.withOpacity(0.2),
          width: 1,
        ),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: AppTheme.lightTheme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w600,
                          color: AppTheme.textPrimaryColor,
                        ),
                      ),
                      Text(
                        subtitle,
                        style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                          color: AppTheme.textSecondaryColor,
                        ),
                      ),
                    ],
                  ),
                ),
                if (onTap != null)
                  Icon(
                    Icons.chevron_right,
                    color: AppTheme.textSecondaryColor.withOpacity(0.5),
                    size: 20,
                  ),
              ],
            ),
            
            const SizedBox(height: 16),
            
            // Chart
            ChartCard(
              title: '',
              subtitle: '',
              chartType: chartType,
              data: data,
              color: color,
            ),
            
            // Legend
            if (showLegend && data.isNotEmpty) ...[
              const SizedBox(height: 16),
              _buildLegend(),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildLegend() {
    return Wrap(
      spacing: 16,
      runSpacing: 8,
      children: data.asMap().entries.map((entry) {
        final index = entry.key;
        final item = entry.value;
        final itemColor = legendColors != null && index < legendColors!.length
            ? legendColors![index]
            : color;

        return Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 12,
              height: 12,
              decoration: BoxDecoration(
                color: itemColor,
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 6),
            Text(
              item['label'] ?? 'Item $index',
              style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                color: AppTheme.textSecondaryColor,
              ),
            ),
          ],
        );
      }).toList(),
    );
  }
}

