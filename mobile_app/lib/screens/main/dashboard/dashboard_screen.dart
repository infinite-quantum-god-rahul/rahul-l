import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import '../../../config/app_routes.dart';
import '../../../config/app_theme.dart';
import '../../../providers/auth_provider.dart';
import '../../../providers/app_provider.dart';
import '../../../widgets/common/custom_button.dart';
import '../../../widgets/common/loading_overlay.dart';
import '../../../widgets/dashboard/metric_card.dart';
import '../../../widgets/dashboard/quick_action_card.dart';
import '../../../widgets/dashboard/recent_activity_card.dart';
import '../../../widgets/dashboard/chart_card.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;
  
  bool _isLoading = false;
  Map<String, dynamic> _dashboardStats = {};
  List<Map<String, dynamic>> _recentActivities = [];
  List<Map<String, dynamic>> _quickActions = [];

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _loadDashboardData();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
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

  Future<void> _loadDashboardData() async {
    try {
      setState(() {
        _isLoading = true;
      });
      
      // Load dashboard statistics
      await _loadDashboardStats();
      
      // Load recent activities
      await _loadRecentActivities();
      
      // Load quick actions
      await _loadQuickActions();
      
    } catch (e) {
      Get.snackbar(
        'Error',
        'Failed to load dashboard data: $e',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: AppTheme.errorColor,
        colorText: Colors.white,
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _loadDashboardStats() async {
    // Simulate API call
    await Future.delayed(const Duration(milliseconds: 500));
    
    setState(() {
      _dashboardStats = {
        'totalClients': 1250,
        'totalLoans': 890,
        'totalDisbursed': 75000000,
        'totalCollected': 68000000,
        'pendingCollections': 7000000,
        'overdueLoans': 45,
        'activeFieldVisits': 23,
        'pendingApprovals': 12,
        'monthlyGrowth': 8.5,
        'recoveryRate': 92.3,
      };
    });
  }

  Future<void> _loadRecentActivities() async {
    // Simulate API call
    await Future.delayed(const Duration(milliseconds: 300));
    
    setState(() {
      _recentActivities = [
        {
          'type': 'loan_approved',
          'title': 'Loan Approved',
          'description': 'Loan #L001234 approved for ₹50,000',
          'timestamp': DateTime.now().subtract(const Duration(minutes: 15)),
          'icon': Icons.check_circle,
          'color': AppTheme.successColor,
        },
        {
          'type': 'payment_received',
          'title': 'Payment Received',
          'description': '₹5,000 received from Client #C001',
          'timestamp': DateTime.now().subtract(const Duration(hours: 2)),
          'icon': Icons.payment,
          'color': AppTheme.primaryColor,
        },
        {
          'type': 'field_visit',
          'title': 'Field Visit Completed',
          'description': 'Visit completed at Village Center #VC001',
          'timestamp': DateTime.now().subtract(const Duration(hours: 4)),
          'icon': Icons.location_on,
          'color': AppTheme.infoColor,
        },
        {
          'type': 'client_added',
          'title': 'New Client Added',
          'description': 'Client #C002 added to the system',
          'timestamp': DateTime.now().subtract(const Duration(hours: 6)),
          'icon': Icons.person_add,
          'color': AppTheme.warningColor,
        },
        {
          'type': 'overdue_alert',
          'title': 'Overdue Alert',
          'description': 'Loan #L001235 is overdue by 5 days',
          'timestamp': DateTime.now().subtract(const Duration(hours: 8)),
          'icon': Icons.warning,
          'color': AppTheme.errorColor,
        },
      ];
    });
  }

  Future<void> _loadQuickActions() async {
    // Simulate API call
    await Future.delayed(const Duration(milliseconds: 200));
    
    setState(() {
      _quickActions = [
        {
          'icon': Icons.person_add,
          'title': 'Add Client',
          'subtitle': 'Register new client',
          'action': () => Get.toNamed(AppRoutes.addClient),
          'color': AppTheme.primaryColor,
        },
        {
          'icon': Icons.add_business,
          'title': 'New Loan',
          'subtitle': 'Create loan application',
          'action': () => Get.toNamed(AppRoutes.newLoan),
          'color': AppTheme.successColor,
        },
        {
          'icon': Icons.location_on,
          'title': 'Field Visit',
          'subtitle': 'Schedule field visit',
          'action': () => Get.toNamed(AppRoutes.addFieldVisit),
          'color': AppTheme.infoColor,
        },
        {
          'icon': Icons.analytics,
          'title': 'Reports',
          'subtitle': 'View analytics',
          'action': () => Get.toNamed(AppRoutes.reports),
          'color': AppTheme.warningColor,
        },
        {
          'icon': Icons.qr_code_scanner,
          'title': 'Scan QR',
          'subtitle': 'Quick client lookup',
          'action': () => Get.toNamed(AppRoutes.qrScanner),
          'color': AppTheme.accentColor,
        },
        {
          'icon': Icons.sync,
          'title': 'Sync Data',
          'subtitle': 'Sync with server',
          'action': () => _syncData(),
          'color': AppTheme.secondaryColor,
        },
      ];
    });
  }

  Future<void> _syncData() async {
    try {
      setState(() {
        _isLoading = true;
      });
      
      // Simulate sync
      await Future.delayed(const Duration(seconds: 2));
      
      Get.snackbar(
        'Success',
        'Data synchronized successfully',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: AppTheme.successColor,
        colorText: Colors.white,
      );
      
      // Reload data
      await _loadDashboardData();
      
    } catch (e) {
      Get.snackbar(
        'Error',
        'Failed to sync data: $e',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: AppTheme.errorColor,
        colorText: Colors.white,
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _refreshData() {
    _loadDashboardData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: LoadingOverlay(
        isLoading: _isLoading,
        child: RefreshIndicator(
          onRefresh: _refreshData,
          child: CustomScrollView(
            slivers: [
              // App Bar
              SliverAppBar(
                expandedHeight: 120,
                floating: false,
                pinned: true,
                backgroundColor: AppTheme.primaryColor,
                flexibleSpace: FlexibleSpaceBar(
                  title: FadeTransition(
                    opacity: _fadeAnimation,
                    child: Text(
                      'Dashboard',
                      style: AppTheme.lightTheme.textTheme.headlineSmall?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  background: Container(
                    decoration: BoxDecoration(
                      gradient: AppTheme.primaryGradient,
                    ),
                  ),
                ),
                actions: [
                  IconButton(
                    onPressed: _refreshData,
                    icon: const Icon(Icons.refresh, color: Colors.white),
                  ),
                  IconButton(
                    onPressed: () => Get.toNamed(AppRoutes.notifications),
                    icon: const Icon(Icons.notifications, color: Colors.white),
                  ),
                ],
              ),
              
              // Dashboard Content
              SliverPadding(
                padding: const EdgeInsets.all(16),
                sliver: SliverList(
                  delegate: SliverChildListDelegate([
                    // Welcome Section
                    FadeTransition(
                      opacity: _fadeAnimation,
                      child: _buildWelcomeSection(),
                    ),
                    
                    const SizedBox(height: 24),
                    
                    // Key Metrics
                    SlideTransition(
                      position: _slideAnimation,
                      child: FadeTransition(
                        opacity: _fadeAnimation,
                        child: _buildKeyMetrics(),
                      ),
                    ),
                    
                    const SizedBox(height: 24),
                    
                    // Quick Actions
                    SlideTransition(
                      position: _slideAnimation,
                      child: FadeTransition(
                        opacity: _fadeAnimation,
                        child: _buildQuickActions(),
                      ),
                    ),
                    
                    const SizedBox(height: 24),
                    
                    // Charts Section
                    SlideTransition(
                      position: _slideAnimation,
                      child: FadeTransition(
                        opacity: _fadeAnimation,
                        child: _buildChartsSection(),
                      ),
                    ),
                    
                    const SizedBox(height: 24),
                    
                    // Recent Activities
                    SlideTransition(
                      position: _slideAnimation,
                      child: FadeTransition(
                        opacity: _fadeAnimation,
                        child: _buildRecentActivities(),
                      ),
                    ),
                    
                    const SizedBox(height: 24),
                    
                    // Quick Stats
                    SlideTransition(
                      position: _slideAnimation,
                      child: FadeTransition(
                        opacity: _fadeAnimation,
                        child: _buildQuickStats(),
                      ),
                    ),
                    
                    const SizedBox(height: 100), // Bottom padding for FAB
                  ]),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildWelcomeSection() {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final user = authProvider.currentUser;
    
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: AppTheme.primaryGradient,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: AppTheme.primaryColor.withOpacity(0.3),
            blurRadius: 20,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              CircleAvatar(
                radius: 25,
                backgroundColor: Colors.white.withOpacity(0.2),
                child: Icon(
                  Icons.person,
                  size: 30,
                  color: Colors.white,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Welcome back,',
                      style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                        color: Colors.white.withOpacity(0.9),
                      ),
                    ),
                    Text(
                      user?.displayName ?? 'User',
                      style: AppTheme.lightTheme.textTheme.headlineSmall?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              Icon(
                Icons.wb_sunny,
                color: Colors.white.withOpacity(0.8),
                size: 24,
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            'Here\'s what\'s happening with your SML operations today',
            style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
              color: Colors.white.withOpacity(0.9),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildKeyMetrics() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Key Metrics',
          style: AppTheme.lightTheme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        GridView.count(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          childAspectRatio: 1.5,
          children: [
            MetricCard(
              title: 'Total Clients',
              value: '${_dashboardStats['totalClients'] ?? 0}',
              subtitle: 'Active clients',
              icon: Icons.people,
              color: AppTheme.primaryColor,
              trend: '+${_dashboardStats['monthlyGrowth'] ?? 0}%',
              isPositive: true,
            ),
            MetricCard(
              title: 'Total Loans',
              value: '${_dashboardStats['totalLoans'] ?? 0}',
              subtitle: 'Active loans',
              icon: Icons.account_balance,
              color: AppTheme.successColor,
              trend: '+${_dashboardStats['monthlyGrowth'] ?? 0}%',
              isPositive: true,
            ),
            MetricCard(
              title: 'Disbursed Amount',
              value: '₹${_formatCurrency(_dashboardStats['totalDisbursed'] ?? 0)}',
              subtitle: 'Total disbursed',
              icon: Icons.trending_up,
              color: AppTheme.infoColor,
              trend: '+${_dashboardStats['monthlyGrowth'] ?? 0}%',
              isPositive: true,
            ),
            MetricCard(
              title: 'Collections',
              value: '₹${_formatCurrency(_dashboardStats['totalCollected'] ?? 0)}',
              subtitle: 'Total collected',
              icon: Icons.payment,
              color: AppTheme.warningColor,
              trend: '${_dashboardStats['recoveryRate'] ?? 0}%',
              isPositive: true,
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildQuickActions() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Quick Actions',
          style: AppTheme.lightTheme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 3,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            childAspectRatio: 1.2,
          ),
          itemCount: _quickActions.length,
          itemBuilder: (context, index) {
            final action = _quickActions[index];
            return QuickActionCard(
              icon: action['icon'],
              title: action['title'],
              subtitle: action['subtitle'],
              color: action['color'],
              onTap: action['action'],
            );
          },
        ),
      ],
    );
  }

  Widget _buildChartsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Analytics',
          style: AppTheme.lightTheme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: ChartCard(
                title: 'Loan Disbursement',
                subtitle: 'Monthly trend',
                chartType: 'line',
                data: _getChartData(),
                color: AppTheme.primaryColor,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: ChartCard(
                title: 'Collections',
                subtitle: 'Recovery rate',
                chartType: 'pie',
                data: _getPieChartData(),
                color: AppTheme.successColor,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildRecentActivities() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'Recent Activities',
              style: AppTheme.lightTheme.textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            TextButton(
              onPressed: () => Get.toNamed(AppRoutes.activities),
              child: Text(
                'View All',
                style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                  color: AppTheme.primaryColor,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: _recentActivities.length,
          itemBuilder: (context, index) {
            final activity = _recentActivities[index];
            return RecentActivityCard(
              type: activity['type'],
              title: activity['title'],
              description: activity['description'],
              timestamp: activity['timestamp'],
              icon: activity['icon'],
              color: activity['color'],
            );
          },
        ),
      ],
    );
  }

  Widget _buildQuickStats() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Quick Stats',
          style: AppTheme.lightTheme.textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: _buildStatCard(
                'Pending Collections',
                '₹${_formatCurrency(_dashboardStats['pendingCollections'] ?? 0)}',
                Icons.pending,
                AppTheme.warningColor,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _buildStatCard(
                'Overdue Loans',
                '${_dashboardStats['overdueLoans'] ?? 0}',
                Icons.warning,
                AppTheme.errorColor,
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: _buildStatCard(
                'Active Visits',
                '${_dashboardStats['activeFieldVisits'] ?? 0}',
                Icons.location_on,
                AppTheme.infoColor,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _buildStatCard(
                'Pending Approvals',
                '${_dashboardStats['pendingApprovals'] ?? 0}',
                Icons.pending_actions,
                AppTheme.secondaryColor,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: color.withOpacity(0.3),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                icon,
                color: color,
                size: 20,
              ),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  title,
                  style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                    color: AppTheme.textSecondaryColor,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: AppTheme.lightTheme.textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  // Helper methods
  String _formatCurrency(int amount) {
    if (amount >= 10000000) {
      return '${(amount / 10000000).toStringAsFixed(1)}Cr';
    } else if (amount >= 100000) {
      return '${(amount / 100000).toStringAsFixed(1)}L';
    } else if (amount >= 1000) {
      return '${(amount / 1000).toStringAsFixed(1)}K';
    }
    return amount.toString();
  }

  List<Map<String, dynamic>> _getChartData() {
    return [
      {'month': 'Jan', 'value': 12000000},
      {'month': 'Feb', 'value': 15000000},
      {'month': 'Mar', 'value': 18000000},
      {'month': 'Apr', 'value': 22000000},
      {'month': 'May', 'value': 25000000},
      {'month': 'Jun', 'value': 28000000},
    ];
  }

  List<Map<String, dynamic>> _getPieChartData() {
    return [
      {'label': 'On Time', 'value': 75, 'color': AppTheme.successColor},
      {'label': 'Late', 'value': 20, 'color': AppTheme.warningColor},
      {'label': 'Overdue', 'value': 5, 'color': AppTheme.errorColor},
    ];
  }
}

