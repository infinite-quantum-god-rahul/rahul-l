import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:fl_chart/fl_chart.dart';

import '../../config/app_theme.dart';
import '../../models/sml_models.dart';
import '../../providers/sml_providers.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../widgets/common/loading_overlay.dart';
import '../../utils/constants.dart';

class EnhancedReportsScreen extends StatefulWidget {
  const EnhancedReportsScreen({Key? key}) : super(key: key);

  @override
  State<EnhancedReportsScreen> createState() => _EnhancedReportsScreenState();
}

class _EnhancedReportsScreenState extends State<EnhancedReportsScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  final TextEditingController _searchController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  String _selectedReportType = 'all';
  String _selectedTimePeriod = 'month';
  String _selectedSortBy = 'date';
  String _selectedSortOrder = 'desc';

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _loadInitialData();
    _setupScrollListener();
  }

  void _initializeAnimations() {
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );

    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));

    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.3),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOutCubic,
    ));

    _animationController.forward();
  }

  void _loadInitialData() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<SMLReportsProvider>().loadDashboardStats();
      context.read<SMLReportsProvider>().loadAnalytics();
    });
  }

  void _setupScrollListener() {
    _scrollController.addListener(() {
      if (_scrollController.position.pixels >=
          _scrollController.position.maxScrollExtent - 200) {
        _loadMoreData();
      }
    });
  }

  void _loadMoreData() {
    final provider = context.read<SMLReportsProvider>();
    if (provider.hasMoreData && !provider.isLoading) {
      provider.loadMoreReports();
    }
  }

  @override
  void dispose() {
    _animationController.dispose();
    _searchController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        body: LoadingOverlay(
          isLoading: context.watch<SMLReportsProvider>().isLoading,
          child: Column(
            children: [
              _buildTabBar(),
              Expanded(
                child: TabBarView(
                  children: [
                    _buildDashboardTab(),
                    _buildAnalyticsTab(),
                    _buildReportsTab(),
                    _buildExportTab(),
                  ],
                ),
              ),
            ],
          ),
        ),
        floatingActionButton: _buildFloatingActionButton(),
      ),
    );
  }

  Widget _buildTabBar() {
    return Container(
      color: AppTheme.primaryColor,
      child: TabBar(
        labelColor: Colors.white,
        unselectedLabelColor: Colors.white70,
        indicatorColor: Colors.white,
        isScrollable: true,
        tabs: const [
          Tab(icon: Icon(Icons.dashboard), text: 'Dashboard'),
          Tab(icon: Icon(Icons.analytics), text: 'Analytics'),
          Tab(icon: Icon(Icons.assessment), text: 'Reports'),
          Tab(icon: Icon(Icons.file_download), text: 'Export'),
        ],
      ),
    );
  }

  Widget _buildDashboardTab() {
    return CustomScrollView(
      controller: _scrollController,
      slivers: [
        _buildDashboardHeader(),
        _buildDashboardMetrics(),
        _buildDashboardCharts(),
        _buildRecentActivities(),
      ],
    );
  }

  Widget _buildAnalyticsTab() {
    return CustomScrollView(
      slivers: [
        _buildAnalyticsHeader(),
        _buildAnalyticsFilters(),
        _buildAnalyticsCharts(),
        _buildAnalyticsInsights(),
      ],
    );
  }

  Widget _buildReportsTab() {
    return CustomScrollView(
      slivers: [
        _buildReportsHeader(),
        _buildReportsList(),
      ],
    );
  }

  Widget _buildExportTab() {
    return CustomScrollView(
      slivers: [
        _buildExportHeader(),
        _buildExportOptions(),
      ],
    );
  }

  Widget _buildDashboardHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.primaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Dashboard', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.primaryGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Total Clients', '0', Icons.people)),
                Expanded(child: _buildQuickStat('Active Loans', '0', Icons.account_balance)),
                Expanded(child: _buildQuickStat('Field Visits', '0', Icons.visibility)),
                Expanded(child: _buildQuickStat('Collections', '0', Icons.payment)),
              ],
            ),
          ),
        ),
      ),
      actions: [
        IconButton(icon: const Icon(Icons.refresh, color: Colors.white), onPressed: _refreshDashboard),
        IconButton(icon: const Icon(Icons.more_vert, color: Colors.white), onPressed: _showDashboardOptions),
      ],
    );
  }

  Widget _buildAnalyticsHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.secondaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Analytics', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.successGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Growth Rate', '0%', Icons.trending_up)),
                Expanded(child: _buildQuickStat('Efficiency', '0%', Icons.speed)),
                Expanded(child: _buildQuickStat('Coverage', '0%', Icons.coverage)),
                Expanded(child: _buildQuickStat('Performance', '0%', Icons.star)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildReportsHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.accentColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Reports', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.warningGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Generated', '0', Icons.file_copy)),
                Expanded(child: _buildQuickStat('Scheduled', '0', Icons.schedule)),
                Expanded(child: _buildQuickStat('Pending', '0', Icons.pending)),
                Expanded(child: _buildQuickStat('Archived', '0', Icons.archive)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildExportHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.infoColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Export', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.infoGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Exported', '0', Icons.file_download)),
                Expanded(child: _buildQuickStat('Formats', '3', Icons.format_list_bulleted)),
                Expanded(child: _buildQuickStat('Scheduled', '0', Icons.schedule)),
                Expanded(child: _buildQuickStat('Templates', '5', Icons.template)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildQuickStat(String label, String value, IconData icon) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon, color: Colors.white70, size: 20),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
        Text(label, style: const TextStyle(color: Colors.white70, fontSize: 12)),
      ],
    );
  }

  Widget _buildDashboardMetrics() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Key Metrics', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            GridView.count(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              childAspectRatio: 1.5,
              children: [
                _buildMetricCard('Portfolio Value', '₹0', '+0%', Icons.account_balance, AppTheme.primaryColor),
                _buildMetricCard('Disbursements', '₹0', '+0%', Icons.payment, AppTheme.successColor),
                _buildMetricCard('Collections', '₹0', '+0%', Icons.account_balance_wallet, AppTheme.accentColor),
                _buildMetricCard('NPA Rate', '0%', '-0%', Icons.warning, AppTheme.errorColor),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricCard(String title, String value, String change, IconData icon, Color color) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: color, size: 24),
                const Spacer(),
                Text(change, style: TextStyle(color: change.startsWith('+') ? Colors.green : Colors.red, fontSize: 12, fontWeight: FontWeight.w600)),
              ],
            ),
            const SizedBox(height: 16),
            Text(value, style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: color)),
            const SizedBox(height: 4),
            Text(title, style: TextStyle(fontSize: 14, color: Colors.grey[600])),
          ],
        ),
      ),
    );
  }

  Widget _buildDashboardCharts() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Performance Charts', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildChartCard('Portfolio Growth', _buildLineChart()),
            const SizedBox(height: 16),
            _buildChartCard('Loan Distribution', _buildPieChart()),
          ],
        ),
      ),
    );
  }

  Widget _buildChartCard(String title, Widget chart) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            SizedBox(height: 200, child: chart),
          ],
        ),
      ),
    );
  }

  Widget _buildLineChart() {
    return LineChart(
      LineChartData(
        gridData: FlGridData(show: true),
        titlesData: FlTitlesData(show: false),
        borderData: FlBorderData(show: true),
        lineBarsData: [
          LineChartBarData(
            spots: [
              const FlSpot(0, 3),
              const FlSpot(2.6, 2),
              const FlSpot(4.9, 5),
              const FlSpot(6.8, 3.1),
              const FlSpot(8, 4),
              const FlSpot(9.5, 3),
              const FlSpot(11, 4),
            ],
            isCurved: true,
            color: AppTheme.primaryColor,
            barWidth: 3,
            dotData: FlDotData(show: false),
          ),
        ],
      ),
    );
  }

  Widget _buildPieChart() {
    return PieChart(
      PieChartData(
        sections: [
          PieChartSectionData(
            value: 40,
            title: 'Personal',
            color: AppTheme.primaryColor,
            radius: 60,
          ),
          PieChartSectionData(
            value: 30,
            title: 'Business',
            color: AppTheme.secondaryColor,
            radius: 60,
          ),
          PieChartSectionData(
            value: 20,
            title: 'Agriculture',
            color: AppTheme.accentColor,
            radius: 60,
          ),
          PieChartSectionData(
            value: 10,
            title: 'Education',
            color: AppTheme.infoColor,
            radius: 60,
          ),
        ],
        centerSpaceRadius: 40,
        sectionsSpace: 2,
      ),
    );
  }

  Widget _buildRecentActivities() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Recent Activities', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildActivityCard('New Loan Application', 'Client: John Doe', '2 hours ago', Icons.add_circle, AppTheme.successColor),
            const SizedBox(height: 8),
            _buildActivityCard('Field Visit Completed', 'Location: Bangalore', '4 hours ago', Icons.check_circle, AppTheme.primaryColor),
            const SizedBox(height: 8),
            _buildActivityCard('Payment Received', 'Amount: ₹50,000', '6 hours ago', Icons.payment, AppTheme.accentColor),
            const SizedBox(height: 8),
            _buildActivityCard('Document Uploaded', 'KYC: Aadhaar Card', '1 day ago', Icons.upload_file, AppTheme.infoColor),
          ],
        ),
      ),
    );
  }

  Widget _buildActivityCard(String title, String subtitle, String time, IconData icon, Color color) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: ListTile(
        leading: CircleAvatar(backgroundColor: color.withOpacity(0.1), child: Icon(icon, color: color)),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(subtitle),
        trailing: Text(time, style: TextStyle(fontSize: 12, color: Colors.grey[500])),
      ),
    );
  }

  Widget _buildAnalyticsFilters() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Analytics Filters', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(child: _buildFilterDropdown('Time Period', _selectedTimePeriod, ['day', 'week', 'month', 'quarter', 'year'], (value) => setState(() => _selectedTimePeriod = value))),
                const SizedBox(width: 16),
                Expanded(child: _buildFilterDropdown('Report Type', _selectedReportType, ['all', 'loans', 'clients', 'field_operations', 'collections'], (value) => setState(() => _selectedReportType = value))),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFilterDropdown(String label, String value, List<String> options, Function(String) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
        const SizedBox(height: 8),
        DropdownButtonFormField<String>(
          value: value,
          decoration: InputDecoration(
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
            contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          ),
          items: options.map((option) => DropdownMenuItem(value: option, child: Text(option.replaceAll('_', ' ').toUpperCase()))).toList(),
          onChanged: (newValue) => onChanged(newValue!),
        ),
      ],
    );
  }

  Widget _buildAnalyticsCharts() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Analytics Charts', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildChartCard('Revenue Trend', _buildAreaChart()),
            const SizedBox(height: 16),
            _buildChartCard('Performance Metrics', _buildBarChart()),
          ],
        ),
      ),
    );
  }

  Widget _buildAreaChart() {
    return AreaChart(
      AreaChartData(
        gridData: FlGridData(show: true),
        titlesData: FlTitlesData(show: false),
        borderData: FlBorderData(show: true),
        areas: [
          AreaChartData(
            spots: [
              const FlSpot(0, 3),
              const FlSpot(2.6, 2),
              const FlSpot(4.9, 5),
              const FlSpot(6.8, 3.1),
              const FlSpot(8, 4),
              const FlSpot(9.5, 3),
              const FlSpot(11, 4),
            ],
            isCurved: true,
            color: AppTheme.primaryColor.withOpacity(0.3),
            borderData: FlBorderData(show: true, color: AppTheme.primaryColor, strokeWidth: 2),
          ),
        ],
      ),
    );
  }

  Widget _buildBarChart() {
    return BarChart(
      BarChartData(
        gridData: FlGridData(show: true),
        titlesData: FlTitlesData(show: false),
        borderData: FlBorderData(show: true),
        barGroups: [
          BarChartGroupData(x: 0, barRods: [BarChartRodData(toY: 8, color: AppTheme.primaryColor)]),
          BarChartGroupData(x: 1, barRods: [BarChartRodData(toY: 10, color: AppTheme.secondaryColor)]),
          BarChartGroupData(x: 2, barRods: [BarChartRodData(toY: 14, color: AppTheme.accentColor)]),
          BarChartGroupData(x: 3, barRods: [BarChartRodData(toY: 15, color: AppTheme.infoColor)]),
          BarChartGroupData(x: 4, barRods: [BarChartRodData(toY: 13, color: AppTheme.warningColor)]),
        ],
      ),
    );
  }

  Widget _buildAnalyticsInsights() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Key Insights', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildInsightCard('Portfolio Growth', 'Your portfolio has grown by 15% this month compared to last month.', Icons.trending_up, AppTheme.successColor),
            const SizedBox(height: 8),
            _buildInsightCard('Collection Efficiency', 'Collection efficiency has improved by 8% due to better field operations.', Icons.analytics, AppTheme.primaryColor),
            const SizedBox(height: 8),
            _buildInsightCard('Risk Assessment', 'NPA rate has decreased by 2% indicating improved risk management.', Icons.security, AppTheme.accentColor),
          ],
        ),
      ),
    );
  }

  Widget _buildInsightCard(String title, String description, IconData icon, Color color) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16)),
                  const SizedBox(height: 4),
                  Text(description, style: TextStyle(fontSize: 14, color: Colors.grey[600])),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildReportsList() {
    return Consumer<SMLReportsProvider>(
      builder: (context, provider, child) {
        if (provider.reports.isEmpty && !provider.isLoading) {
          return _buildEmptyReportsState();
        }

        return SliverList(
          delegate: SliverChildBuilderDelegate(
            (context, index) {
              if (index >= provider.reports.length) {
                if (provider.hasMoreData) {
                  return _buildLoadingMore();
                }
                return const SizedBox.shrink();
              }

              final report = provider.reports[index];
              return _buildReportCard(report);
            },
            childCount: provider.reports.length + (provider.hasMoreData ? 1 : 0),
          ),
        );
      },
    );
  }

  Widget _buildReportCard(dynamic report) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
          child: Icon(Icons.assessment, color: AppTheme.primaryColor),
        ),
        title: Text('Report ${report.id ?? 'N/A'}', style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text('Generated on ${DateTime.now().toString().substring(0, 10)}'),
        trailing: PopupMenuButton(
          itemBuilder: (context) => [
            const PopupMenuItem(value: 'view', child: Text('View')),
            const PopupMenuItem(value: 'download', child: Text('Download')),
            const PopupMenuItem(value: 'share', child: Text('Share')),
            const PopupMenuItem(value: 'delete', child: Text('Delete')),
          ],
          onSelected: (value) => _handleReportAction(value, report),
        ),
      ),
    );
  }

  Widget _buildEmptyReportsState() {
    return SliverFillRemaining(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.assessment_outlined, size: 80, color: Colors.grey[400]),
            const SizedBox(height: 16),
            Text('No Reports Found', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.grey[600])),
            const SizedBox(height: 8),
            Text('Generate your first report to get started', style: TextStyle(fontSize: 16, color: Colors.grey[500]), textAlign: TextAlign.center),
            const SizedBox(height: 24),
            CustomButton(text: 'Generate Report', onPressed: _generateNewReport, icon: Icons.add, style: CustomButtonStyle.primary),
          ],
        ),
      ),
    );
  }

  Widget _buildExportOptions() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Export Options', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildExportOption('Client Data', 'Export client information and details', Icons.people, () => _exportClientData()),
            const SizedBox(height: 8),
            _buildExportOption('Loan Portfolio', 'Export loan portfolio and performance data', Icons.account_balance, () => _exportLoanPortfolio()),
            const SizedBox(height: 8),
            _buildExportOption('Field Operations', 'Export field visit and schedule data', Icons.visibility, () => _exportFieldOperations()),
            const SizedBox(height: 8),
            _buildExportOption('Financial Reports', 'Export financial statements and reports', Icons.assessment, () => _exportFinancialReports()),
            const SizedBox(height: 8),
            _buildExportOption('Custom Report', 'Create and export custom reports', Icons.create, () => _exportCustomReport()),
          ],
        ),
      ),
    );
  }

  Widget _buildExportOption(String title, String description, IconData icon, VoidCallback onTap) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Icon(icon, color: AppTheme.primaryColor, size: 24),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16)),
                    const SizedBox(height: 4),
                    Text(description, style: TextStyle(fontSize: 14, color: Colors.grey[600])),
                  ],
                ),
              ),
              Icon(Icons.arrow_forward_ios, color: Colors.grey[400], size: 16),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLoadingMore() {
    return const Padding(
      padding: EdgeInsets.all(16),
      child: Center(child: CircularProgressIndicator()),
    );
  }

  Widget _buildFloatingActionButton() {
    return FloatingActionButton.extended(
      onPressed: _generateNewReport,
      icon: const Icon(Icons.add),
      label: const Text('Generate Report'),
      backgroundColor: AppTheme.primaryColor,
      foregroundColor: Colors.white,
    );
  }

  // Event handlers
  void _refreshDashboard() => context.read<SMLReportsProvider>().loadDashboardStats();
  void _showDashboardOptions() => _showOptionsMenu('Dashboard Options');
  void _generateNewReport() => Get.toNamed('/generate-report');
  void _exportClientData() => _showExportDialog('Client Data');
  void _exportLoanPortfolio() => _showExportDialog('Loan Portfolio');
  void _exportFieldOperations() => _showExportDialog('Field Operations');
  void _exportFinancialReports() => _showExportDialog('Financial Reports');
  void _exportCustomReport() => Get.toNamed('/custom-report');

  void _handleReportAction(String action, dynamic report) {
    switch (action) {
      case 'view':
        Get.toNamed('/view-report', arguments: report);
        break;
      case 'download':
        _downloadReport(report);
        break;
      case 'share':
        _shareReport(report);
        break;
      case 'delete':
        _deleteReport(report);
        break;
    }
  }

  void _downloadReport(dynamic report) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Downloading report ${report.id}...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _shareReport(dynamic report) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Sharing report ${report.id}...'), backgroundColor: AppTheme.successColor),
    );
  }

  void _deleteReport(dynamic report) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Report'),
        content: Text('Are you sure you want to delete report ${report.id}?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Report ${report.id} deleted'), backgroundColor: AppTheme.errorColor),
              );
            },
            child: const Text('Delete', style: TextStyle(color: AppTheme.errorColor)),
          ),
        ],
      ),
    );
  }

  void _showOptionsMenu(String title) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildOptionsSheet(title),
    );
  }

  Widget _buildOptionsSheet(String title) {
    return Container(
      decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                IconButton(onPressed: () => Navigator.pop(context), icon: const Icon(Icons.close)),
              ],
            ),
            const SizedBox(height: 20),
            _buildOptionTile('Settings', Icons.settings, () { Navigator.pop(context); Get.toNamed('/settings'); }),
            _buildOptionTile('Help & Support', Icons.help, () { Navigator.pop(context); Get.toNamed('/help-support'); }),
            _buildOptionTile('About', Icons.info, () { Navigator.pop(context); _showAboutDialog(); }),
          ],
        ),
      ),
    );
  }

  Widget _buildOptionTile(String title, IconData icon, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: AppTheme.primaryColor),
      title: Text(title),
      onTap: onTap,
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
    );
  }

  void _showExportDialog(String dataType) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Export $dataType'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Select export format:'),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildFormatButton('PDF', Icons.picture_as_pdf, () => _exportAsPDF(dataType)),
                _buildFormatButton('Excel', Icons.table_chart, () => _exportAsExcel(dataType)),
                _buildFormatButton('CSV', Icons.table_view, () => _exportAsCSV(dataType)),
              ],
            ),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
        ],
      ),
    );
  }

  Widget _buildFormatButton(String label, IconData icon, VoidCallback onPressed) {
    return Column(
      children: [
        IconButton(
          onPressed: onPressed,
          icon: Icon(icon, size: 32),
          color: AppTheme.primaryColor,
        ),
        Text(label, style: const TextStyle(fontSize: 12)),
      ],
    );
  }

  void _exportAsPDF(String dataType) {
    Navigator.pop(context);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Exporting $dataType as PDF...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _exportAsExcel(String dataType) {
    Navigator.pop(context);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Exporting $dataType as Excel...'), backgroundColor: AppTheme.successColor),
    );
  }

  void _exportAsCSV(String dataType) {
    Navigator.pop(context);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Exporting $dataType as CSV...'), backgroundColor: AppTheme.accentColor),
    );
  }

  void _showAboutDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('About Reports & Analytics'),
        content: const Text('This module provides comprehensive reporting and analytics capabilities including dashboard metrics, performance charts, custom reports, and data export functionality.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('OK')),
        ],
      ),
    );
  }
}

