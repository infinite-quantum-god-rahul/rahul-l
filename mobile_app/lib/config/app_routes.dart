import 'package:get/get.dart';
import '../screens/splash_screen.dart';
import '../screens/auth/login_screen.dart';
import '../screens/auth/otp_screen.dart';
import '../screens/auth/forgot_password_screen.dart';
import '../screens/auth/biometric_setup_screen.dart';
import '../screens/main/dashboard_screen.dart';
import '../screens/main/main_navigation_screen.dart';
import '../screens/clients/client_list_screen.dart';
import '../screens/clients/client_detail_screen.dart';
import '../screens/clients/client_registration_screen.dart';
import '../screens/loans/loan_list_screen.dart';
import '../screens/loans/loan_detail_screen.dart';
import '../screens/loans/loan_application_screen.dart';
import '../screens/loans/emi_calculator_screen.dart';
import '../screens/field/field_schedule_screen.dart';
import '../screens/field/field_visit_screen.dart';
import '../screens/field/visit_recording_screen.dart';
import '../screens/reports/reports_screen.dart';
import '../screens/reports/analytics_screen.dart';
import '../screens/profile/profile_screen.dart';
import '../screens/profile/settings_screen.dart';
import '../screens/profile/help_support_screen.dart';
import '../screens/common/document_upload_screen.dart';
import '../screens/common/qr_scanner_screen.dart';
import '../screens/common/offline_sync_screen.dart';

class AppRoutes {
  // Route Names
  static const String splash = '/splash';
  static const String login = '/login';
  static const String otp = '/otp';
  static const String forgotPassword = '/forgot-password';
  static const String biometricSetup = '/biometric-setup';
  static const String dashboard = '/dashboard';
  static const String mainNavigation = '/main-navigation';
  
  // Client Routes
  static const String clientList = '/clients';
  static const String clientDetail = '/clients/detail';
  static const String clientRegistration = '/clients/register';
  
  // Loan Routes
  static const String loanList = '/loans';
  static const String loanDetail = '/loans/detail';
  static const String loanApplication = '/loans/apply';
  static const String emiCalculator = '/loans/emi-calculator';
  
  // Field Operation Routes
  static const String fieldSchedule = '/field/schedule';
  static const String fieldVisit = '/field/visit';
  static const String visitRecording = '/field/recording';
  
  // Report Routes
  static const String reports = '/reports';
  static const String analytics = '/reports/analytics';
  
  // Profile Routes
  static const String profile = '/profile';
  static const String settings = '/profile/settings';
  static const String helpSupport = '/profile/help';
  
  // Common Routes
  static const String documentUpload = '/common/upload';
  static const String qrScanner = '/common/scanner';
  static const String offlineSync = '/common/sync';
  
  // Get Pages Configuration
  static List<GetPage> get getPages => [
    // Splash Screen
    GetPage(
      name: splash,
      page: () => const SplashScreen(),
      transition: Transition.fadeIn,
      transitionDuration: const Duration(milliseconds: 500),
    ),
    
    // Authentication Screens
    GetPage(
      name: login,
      page: () => const LoginScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: otp,
      page: () => const OTPScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: forgotPassword,
      page: () => const ForgotPasswordScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: biometricSetup,
      page: () => const BiometricSetupScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    // Main App Screens
    GetPage(
      name: dashboard,
      page: () => const DashboardScreen(),
      transition: Transition.fadeIn,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: mainNavigation,
      page: () => const MainNavigationScreen(),
      transition: Transition.fadeIn,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    // Client Management Screens
    GetPage(
      name: clientList,
      page: () => const ClientListScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: clientDetail,
      page: () => const ClientDetailScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: clientRegistration,
      page: () => const ClientRegistrationScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    // Loan Management Screens
    GetPage(
      name: loanList,
      page: () => const LoanListScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: loanDetail,
      page: () => const LoanDetailScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: loanApplication,
      page: () => const LoanApplicationScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: emiCalculator,
      page: () => const EMICalculatorScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    // Field Operations Screens
    GetPage(
      name: fieldSchedule,
      page: () => const FieldScheduleScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: fieldVisit,
      page: () => const FieldVisitScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: visitRecording,
      page: () => const VisitRecordingScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    // Reports & Analytics Screens
    GetPage(
      name: reports,
      page: () => const ReportsScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: analytics,
      page: () => const AnalyticsScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    // Profile & Settings Screens
    GetPage(
      name: profile,
      page: () => const ProfileScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: settings,
      page: () => const SettingsScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: helpSupport,
      page: () => const HelpSupportScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    // Common Utility Screens
    GetPage(
      name: documentUpload,
      page: () => const DocumentUploadScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: qrScanner,
      page: () => const QRScannerScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    
    GetPage(
      name: offlineSync,
      page: () => const OfflineSyncScreen(),
      transition: Transition.rightToLeft,
      transitionDuration: const Duration(milliseconds: 300),
    ),
  ];
  
  // Navigation Helper Methods
  static void goToSplash() => Get.offAllNamed(splash);
  static void goToLogin() => Get.offAllNamed(login);
  static void goToDashboard() => Get.offAllNamed(dashboard);
  static void goToMainNavigation() => Get.offAllNamed(mainNavigation);
  
  // Client Navigation
  static void goToClientList() => Get.toNamed(clientList);
  static void goToClientDetail(String clientId) => Get.toNamed(clientDetail, arguments: {'clientId': clientId});
  static void goToClientRegistration() => Get.toNamed(clientRegistration);
  
  // Loan Navigation
  static void goToLoanList() => Get.toNamed(loanList);
  static void goToLoanDetail(String loanId) => Get.toNamed(loanDetail, arguments: {'loanId': loanId});
  static void goToLoanApplication() => Get.toNamed(loanApplication);
  static void goToEMICalculator() => Get.toNamed(emiCalculator);
  
  // Field Operations Navigation
  static void goToFieldSchedule() => Get.toNamed(fieldSchedule);
  static void goToFieldVisit(String visitId) => Get.toNamed(fieldVisit, arguments: {'visitId': visitId});
  static void goToVisitRecording(String visitId) => Get.toNamed(visitRecording, arguments: {'visitId': visitId});
  
  // Reports Navigation
  static void goToReports() => Get.toNamed(reports);
  static void goToAnalytics() => Get.toNamed(analytics);
  
  // Profile Navigation
  static void goToProfile() => Get.toNamed(profile);
  static void goToSettings() => Get.toNamed(settings);
  static void goToHelpSupport() => Get.toNamed(helpSupport);
  
  // Common Navigation
  static void goToDocumentUpload() => Get.toNamed(documentUpload);
  static void goToQRScanner() => Get.toNamed(qrScanner);
  static void goToOfflineSync() => Get.toNamed(offlineSync);
  
  // Back Navigation
  static void goBack() => Get.back();
  static void goBackTo(String route) => Get.until((route) => route.settings.name == route);
  
  // Route Guards
  static bool isAuthenticatedRoute(String route) {
    final publicRoutes = [splash, login, otp, forgotPassword, biometricSetup];
    return !publicRoutes.contains(route);
  }
  
  static bool requiresBiometric(String route) {
    final biometricRoutes = [dashboard, mainNavigation, clientList, loanList, fieldSchedule];
    return biometricRoutes.contains(route);
  }
  
  // Route Parameters
  static Map<String, dynamic>? getRouteArguments() {
    return Get.arguments as Map<String, dynamic>?;
  }
  
  static String? getRouteArgument(String key) {
    final args = getRouteArguments();
    return args?[key] as String?;
  }
  
  // Route History
  static List<String> getRouteHistory() {
    return Get.routing.current;
  }
  
  static bool hasRouteInHistory(String route) {
    return getRouteHistory().contains(route);
  }
  
  // Deep Linking
  static void handleDeepLink(String link) {
    // Parse deep link and navigate accordingly
    if (link.startsWith('sml://client/')) {
      final clientId = link.split('/').last;
      goToClientDetail(clientId);
    } else if (link.startsWith('sml://loan/')) {
      final loanId = link.split('/').last;
      goToLoanDetail(loanId);
    } else if (link.startsWith('sml://field/')) {
      final visitId = link.split('/').last;
      goToFieldVisit(visitId);
    }
  }
  
  // Route Analytics
  static void trackRouteChange(String from, String to) {
    // Implement analytics tracking for route changes
    print('Route changed from $from to $to');
  }
  
  // Route Validation
  static bool isValidRoute(String route) {
    return getPages.any((page) => page.name == route);
  }
  
  // Route Permissions
  static bool hasRoutePermission(String route, List<String> userPermissions) {
    // Implement permission-based route access
    final adminRoutes = [analytics, settings];
    final staffRoutes = [clientRegistration, loanApplication, fieldVisit];
    
    if (adminRoutes.contains(route)) {
      return userPermissions.contains('admin');
    } else if (staffRoutes.contains(route)) {
      return userPermissions.contains('staff') || userPermissions.contains('admin');
    }
    
    return true; // Default allow
  }
}

