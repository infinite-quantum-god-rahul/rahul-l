import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import '../../config/app_routes.dart';
import '../../config/app_theme.dart';
import '../../providers/auth_provider.dart';
import '../../providers/app_provider.dart';
import '../../widgets/common/loading_overlay.dart';
import 'dashboard/dashboard_screen.dart';
import 'clients/client_list_screen.dart';
import 'loans/loan_list_screen.dart';
import 'field/field_schedule_screen.dart';
import 'reports/reports_screen.dart';
import 'profile/profile_screen.dart';

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({Key? key}) : super(key: key);

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen>
    with TickerProviderStateMixin {
  int _currentIndex = 0;
  late PageController _pageController;
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  
  final List<Widget> _screens = [
    const DashboardScreen(),
    const ClientListScreen(),
    const LoanListScreen(),
    const FieldScheduleScreen(),
    const ReportsScreen(),
    const ProfileScreen(),
  ];

  final List<BottomNavigationBarItem> _bottomNavItems = [
    const BottomNavigationBarItem(
      icon: Icon(Icons.dashboard),
      label: 'Dashboard',
    ),
    const BottomNavigationBarItem(
      icon: Icon(Icons.people),
      label: 'Clients',
    ),
    const BottomNavigationBarItem(
      icon: Icon(Icons.account_balance),
      label: 'Loans',
    ),
    const BottomNavigationBarItem(
      icon: Icon(Icons.location_on),
      label: 'Field',
    ),
    const BottomNavigationBarItem(
      icon: Icon(Icons.analytics),
      label: 'Reports',
    ),
    const BottomNavigationBarItem(
      icon: Icon(Icons.person),
      label: 'Profile',
    ),
  ];

  @override
  void initState() {
    super.initState();
    _initializeControllers();
    _initializeProviders();
  }

  @override
  void dispose() {
    _pageController.dispose();
    _animationController.dispose();
    super.dispose();
  }

  void _initializeControllers() {
    _pageController = PageController(initialPage: _currentIndex);
    
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    
    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));
    
    _animationController.forward();
  }

  Future<void> _initializeProviders() async {
    final appProvider = Provider.of<AppProvider>(context, listen: false);
    await appProvider.initialize();
  }

  void _onTabTapped(int index) {
    if (_currentIndex != index) {
      setState(() {
        _currentIndex = index;
      });
      
      _pageController.animateToPage(
        index,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
      
      // Trigger animation
      _animationController.reset();
      _animationController.forward();
    }
  }

  void _onPageChanged(int index) {
    setState(() {
      _currentIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: LoadingOverlay(
        isLoading: false,
        child: FadeTransition(
          opacity: _fadeAnimation,
          child: PageView(
            controller: _pageController,
            onPageChanged: _onPageChanged,
            children: _screens,
          ),
        ),
      ),
      bottomNavigationBar: _buildBottomNavigationBar(),
      floatingActionButton: _buildFloatingActionButton(),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
    );
  }

  Widget _buildBottomNavigationBar() {
    return Container(
      decoration: BoxDecoration(
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 20,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: _onTabTapped,
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.white,
        selectedItemColor: AppTheme.primaryColor,
        unselectedItemColor: AppTheme.textSecondaryColor,
        selectedLabelStyle: AppTheme.lightTheme.textTheme.labelSmall?.copyWith(
          fontWeight: FontWeight.w600,
        ),
        unselectedLabelStyle: AppTheme.lightTheme.textTheme.labelSmall,
        elevation: 0,
        items: _bottomNavItems,
      ),
    );
  }

  Widget? _buildFloatingActionButton() {
    // Show FAB only on specific screens
    if (_currentIndex == 1) { // Clients screen
      return FloatingActionButton(
        onPressed: () => _showQuickActionMenu(context),
        backgroundColor: AppTheme.primaryColor,
        foregroundColor: Colors.white,
        elevation: 8,
        child: const Icon(Icons.add),
      );
    } else if (_currentIndex == 2) { // Loans screen
      return FloatingActionButton(
        onPressed: () => _showQuickActionMenu(context),
        backgroundColor: AppTheme.primaryColor,
        foregroundColor: Colors.white,
        elevation: 8,
        child: const Icon(Icons.add),
      );
    } else if (_currentIndex == 3) { // Field operations screen
      return FloatingActionButton(
        onPressed: () => _showQuickActionMenu(context),
        backgroundColor: AppTheme.primaryColor,
        foregroundColor: Colors.white,
        elevation: 8,
        child: const Icon(Icons.add),
      );
    }
    
    return null;
  }

  void _showQuickActionMenu(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildQuickActionSheet(),
    );
  }

  Widget _buildQuickActionSheet() {
    final actions = _getQuickActions();
    
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Handle
          Container(
            margin: const EdgeInsets.only(top: 12),
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: AppTheme.textSecondaryColor.withOpacity(0.3),
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          
          const SizedBox(height: 20),
          
          // Title
          Text(
            'Quick Actions',
            style: AppTheme.lightTheme.textTheme.titleLarge?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          
          const SizedBox(height: 20),
          
          // Actions Grid
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            child: GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 3,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                childAspectRatio: 1.2,
              ),
              itemCount: actions.length,
              itemBuilder: (context, index) {
                final action = actions[index];
                return _buildQuickActionItem(action);
              },
            ),
          ),
          
          const SizedBox(height: 20),
          
          // Cancel Button
          Padding(
            padding: const EdgeInsets.only(bottom: 20),
            child: TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text(
                'Cancel',
                style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                  color: AppTheme.textSecondaryColor,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  List<Map<String, dynamic>> _getQuickActions() {
    switch (_currentIndex) {
      case 1: // Clients
        return [
          {
            'icon': Icons.person_add,
            'label': 'Add Client',
            'action': () => _navigateToAddClient(),
          },
          {
            'icon': Icons.search,
            'label': 'Search',
            'action': () => _showSearchDialog(),
          },
          {
            'icon': Icons.filter_list,
            'label': 'Filter',
            'action': () => _showFilterDialog(),
          },
          {
            'icon': Icons.import_export,
            'label': 'Import',
            'action': () => _showImportDialog(),
          },
          {
            'icon': Icons.download,
            'label': 'Export',
            'action': () => _showExportDialog(),
          },
          {
            'icon': Icons.qr_code_scanner,
            'label': 'Scan QR',
            'action': () => _navigateToQRScanner(),
          },
        ];
        
      case 2: // Loans
        return [
          {
            'icon': Icons.add_business,
            'label': 'New Loan',
            'action': () => _navigateToNewLoan(),
          },
          {
            'icon': Icons.search,
            'label': 'Search',
            'action': () => _showSearchDialog(),
          },
          {
            'icon': Icons.filter_list,
            'label': 'Filter',
            'action': () => _showFilterDialog(),
          },
          {
            'icon': Icons.schedule,
            'label': 'Schedule',
            'action': () => _navigateToLoanSchedule(),
          },
          {
            'icon': Icons.payment,
            'label': 'Payment',
            'action': () => _navigateToPayment(),
          },
          {
            'icon': Icons.analytics,
            'label': 'Analytics',
            'action': () => _navigateToLoanAnalytics(),
          },
        ];
        
      case 3: // Field Operations
        return [
          {
            'icon': Icons.add_location,
            'label': 'Add Visit',
            'action': () => _navigateToAddVisit(),
          },
          {
            'icon': Icons.schedule,
            'label': 'Schedule',
            'action': () => _navigateToFieldSchedule(),
          },
          {
            'icon': Icons.map,
            'label': 'Map View',
            'action': () => _navigateToMapView(),
          },
          {
            'icon': Icons.camera_alt,
            'label': 'Photo',
            'action': () => _navigateToPhotoCapture(),
          },
          {
            'icon': Icons.gps_fixed,
            'label': 'Location',
            'action': () => _getCurrentLocation(),
          },
          {
            'icon': Icons.offline_pin,
            'label': 'Offline',
            'action': () => _toggleOfflineMode(),
          },
        ];
        
      default:
        return [];
    }
  }

  Widget _buildQuickActionItem(Map<String, dynamic> action) {
    return InkWell(
      onTap: () {
        Navigator.pop(context);
        action['action']();
      },
      borderRadius: BorderRadius.circular(12),
      child: Container(
        decoration: BoxDecoration(
          color: AppTheme.primaryColor.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: AppTheme.primaryColor.withOpacity(0.2),
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              action['icon'],
              size: 28,
              color: AppTheme.primaryColor,
            ),
            const SizedBox(height: 8),
            Text(
              action['label'],
              style: AppTheme.lightTheme.textTheme.labelSmall?.copyWith(
                color: AppTheme.primaryColor,
                fontWeight: FontWeight.w500,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  // Navigation methods
  void _navigateToAddClient() {
    Get.toNamed(AppRoutes.addClient);
  }

  void _navigateToNewLoan() {
    Get.toNamed(AppRoutes.newLoan);
  }

  void _navigateToAddVisit() {
    Get.toNamed(AppRoutes.addFieldVisit);
  }

  void _navigateToFieldSchedule() {
    Get.toNamed(AppRoutes.fieldSchedule);
  }

  void _navigateToLoanSchedule() {
    Get.toNamed(AppRoutes.loanSchedule);
  }

  void _navigateToPayment() {
    Get.toNamed(AppRoutes.payment);
  }

  void _navigateToLoanAnalytics() {
    Get.toNamed(AppRoutes.loanAnalytics);
  }

  void _navigateToMapView() {
    Get.toNamed(AppRoutes.mapView);
  }

  void _navigateToPhotoCapture() {
    Get.toNamed(AppRoutes.photoCapture);
  }

  void _navigateToQRScanner() {
    Get.toNamed(AppRoutes.qrScanner);
  }

  // Action methods
  void _showSearchDialog() {
    // Implement search dialog
    Get.snackbar(
      'Search',
      'Search functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _showFilterDialog() {
    // Implement filter dialog
    Get.snackbar(
      'Filter',
      'Filter functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _showImportDialog() {
    // Implement import dialog
    Get.snackbar(
      'Import',
      'Import functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _showExportDialog() {
    // Implement export dialog
    Get.snackbar(
      'Export',
      'Export functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _getCurrentLocation() {
    // Implement location functionality
    Get.snackbar(
      'Location',
      'Getting current location...',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _toggleOfflineMode() {
    // Implement offline mode toggle
    Get.snackbar(
      'Offline Mode',
      'Offline mode toggled',
      snackPosition: SnackPosition.BOTTOM,
    );
  }
}
