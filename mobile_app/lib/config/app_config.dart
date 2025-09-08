class AppConfig {
  // App Information
  static const String appName = 'SML Professional';
  static const String appVersion = '1.0.0';
  static const String appBuildNumber = '1';
  static const String appDescription = 'Enterprise-grade mobile application for Spoorthi MACS Ltd.';
  
  // Company Information
  static const String companyName = 'Spoorthi MACS Ltd.';
  static const String companyWebsite = 'https://www.sml.com';
  static const String companyEmail = 'support@sml.com';
  static const String companyPhone = '+91-XXXXXXXXXX';
  
  // API Configuration
  static const String apiBaseUrl = 'http://127.0.0.1:8000/api/';
  static const String apiVersion = 'v1';
  static const int apiTimeout = 30000; // 30 seconds
  static const int apiRetryAttempts = 3;
  
  // Authentication
  static const String authTokenKey = 'auth_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userDataKey = 'user_data';
  static const int sessionTimeout = 3600000; // 1 hour in milliseconds
  static const bool enableBiometric = true;
  
  // Security
  static const String encryptionKey = 'sml_professional_2024';
  static const bool enableSSL = true;
  static const bool enableCertificatePinning = true;
  static const List<String> allowedHosts = [
    '127.0.0.1',
    'localhost',
    'sml.com',
    'api.sml.com',
  ];
  
  // Database
  static const String hiveBoxName = 'sml_professional';
  static const String userBoxName = 'users';
  static const String clientBoxName = 'clients';
  static const String loanBoxName = 'loans';
  static const String fieldBoxName = 'field_operations';
  
  // File Storage
  static const String documentsPath = '/documents';
  static const String imagesPath = '/images';
  static const String tempPath = '/temp';
  static const int maxFileSize = 10485760; // 10MB
  static const List<String> allowedImageTypes = ['jpg', 'jpeg', 'png', 'pdf'];
  
  // Offline Support
  static const bool enableOfflineMode = true;
  static const int maxOfflineDataAge = 604800000; // 7 days in milliseconds
  static const int syncInterval = 300000; // 5 minutes
  
  // Notifications
  static const String notificationChannelId = 'sml_notifications';
  static const String notificationChannelName = 'SML Notifications';
  static const String notificationChannelDescription = 'Important updates from SML Professional';
  
  // Maps & Location
  static const String googleMapsApiKey = 'YOUR_GOOGLE_MAPS_API_KEY';
  static const double defaultLatitude = 12.9716; // Bangalore
  static const double defaultLongitude = 77.5946;
  static const int locationAccuracy = 10; // meters
  
  // UI Configuration
  static const double defaultPadding = 16.0;
  static const double defaultMargin = 16.0;
  static const double defaultRadius = 8.0;
  static const Duration defaultAnimationDuration = Duration(milliseconds: 300);
  
  // Pagination
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;
  
  // Cache Configuration
  static const int imageCacheExpiry = 86400000; // 24 hours
  static const int dataCacheExpiry = 3600000; // 1 hour
  static const int maxCacheSize = 104857600; // 100MB
  
  // Error Handling
  static const bool enableCrashReporting = true;
  static const bool enableAnalytics = true;
  static const String crashReportingUrl = 'https://crash.sml.com';
  
  // Feature Flags
  static const bool enableQRCodeScanning = true;
  static const bool enableBiometricAuth = true;
  static const bool enableOfflineForms = true;
  static const bool enableRealTimeUpdates = true;
  static const bool enableAdvancedAnalytics = true;
  
  // Development
  static const bool isDevelopment = true;
  static const bool enableDebugLogs = true;
  static const bool enablePerformanceMonitoring = true;
  
  // Support
  static const String supportEmail = 'support@sml.com';
  static const String supportPhone = '+91-XXXXXXXXXX';
  static const String supportWhatsApp = '+91-XXXXXXXXXX';
  static const String helpCenterUrl = 'https://help.sml.com';
  
  // Legal
  static const String privacyPolicyUrl = 'https://www.sml.com/privacy';
  static const String termsOfServiceUrl = 'https://www.sml.com/terms';
  static const String dataProtectionUrl = 'https://www.sml.com/data-protection';
  
  // App Store
  static const String playStoreUrl = 'https://play.google.com/store/apps/details?id=com.sml.professional';
  static const String appStoreUrl = 'https://apps.apple.com/app/sml-professional/id123456789';
  
  // Social Media
  static const String facebookUrl = 'https://facebook.com/smlprofessional';
  static const String twitterUrl = 'https://twitter.com/smlprofessional';
  static const String linkedinUrl = 'https://linkedin.com/company/smlprofessional';
  static const String instagramUrl = 'https://instagram.com/smlprofessional';
  
  // Version Check
  static const bool enableAutoUpdate = true;
  static const String updateCheckUrl = 'https://api.sml.com/version/check';
  
  // Backup & Sync
  static const bool enableAutoBackup = true;
  static const int backupInterval = 86400000; // 24 hours
  static const String backupUrl = 'https://api.sml.com/backup';
  
  // Performance
  static const int maxConcurrentRequests = 5;
  static const int requestQueueSize = 100;
  static const bool enableRequestCaching = true;
  
  // Localization
  static const String defaultLanguage = 'en';
  static const String defaultCountry = 'IN';
  static const List<String> supportedLanguages = ['en', 'hi', 'kn'];
  static const List<String> supportedCountries = ['IN'];
  
  // Accessibility
  static const bool enableVoiceOver = true;
  static const bool enableHighContrast = true;
  static const bool enableLargeText = true;
  static const double minTouchTargetSize = 48.0;
  
  // Network
  static const bool enableCellularData = true;
  static const bool enableWiFiOnly = false;
  static const int networkTimeout = 30000; // 30 seconds
  static const bool enableNetworkMonitoring = true;
}

