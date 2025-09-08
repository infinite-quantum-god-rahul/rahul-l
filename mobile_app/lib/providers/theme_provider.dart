import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../config/app_theme.dart';
import '../utils/constants.dart';

class ThemeProvider extends ChangeNotifier {
  ThemeMode _themeMode = ThemeMode.light;
  bool _isDarkMode = false;
  bool _useSystemTheme = true;
  bool _useHighContrast = false;
  bool _useLargeText = false;
  bool _useReducedMotion = false;
  double _fontScale = 1.0;
  Color _accentColor = AppTheme.accentColor;
  String _fontFamily = AppTheme.defaultFontFamily;

  // Getters
  ThemeMode get themeMode => _themeMode;
  bool get isDarkMode => _isDarkMode;
  bool get useSystemTheme => _useSystemTheme;
  bool get useHighContrast => _useHighContrast;
  bool get useLargeText => _useLargeText;
  bool get useReducedMotion => _useReducedMotion;
  double get fontScale => _fontScale;
  Color get accentColor => _accentColor;
  String get fontFamily => _fontFamily;

  // Initialize theme
  Future<void> initialize() async {
    try {
      // Load saved theme preferences
      await _loadThemePreferences();
      
      // Apply theme
      _applyTheme();
    } catch (e) {
      // Use default theme if loading fails
      _themeMode = ThemeMode.light;
      _isDarkMode = false;
      _useSystemTheme = true;
      _useHighContrast = false;
      _useLargeText = false;
      _useReducedMotion = false;
      _fontScale = 1.0;
      _accentColor = AppTheme.accentColor;
      _fontFamily = AppTheme.defaultFontFamily;
    }
  }

  // Load theme preferences
  Future<void> _loadThemePreferences() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      
      _useSystemTheme = prefs.getBool(AppConstants.useSystemThemeKey) ?? true;
      _useHighContrast = prefs.getBool(AppConstants.useHighContrastKey) ?? false;
      _useLargeText = prefs.getBool(AppConstants.useLargeTextKey) ?? false;
      _useReducedMotion = prefs.getBool(AppConstants.useReducedMotionKey) ?? false;
      _fontScale = prefs.getDouble(AppConstants.fontScaleKey) ?? 1.0;
      
      final savedThemeMode = prefs.getString(AppConstants.themeModeKey);
      if (savedThemeMode != null) {
        switch (savedThemeMode) {
          case 'light':
            _themeMode = ThemeMode.light;
            _isDarkMode = false;
            break;
          case 'dark':
            _themeMode = ThemeMode.dark;
            _isDarkMode = true;
            break;
          case 'system':
            _themeMode = ThemeMode.system;
            _isDarkMode = _getSystemThemeMode() == ThemeMode.dark;
            break;
        }
      }
      
      final savedAccentColor = prefs.getInt(AppConstants.accentColorKey);
      if (savedAccentColor != null) {
        _accentColor = Color(savedAccentColor);
      }
      
      final savedFontFamily = prefs.getString(AppConstants.fontFamilyKey);
      if (savedFontFamily != null) {
        _fontFamily = savedFontFamily;
      }
    } catch (e) {
      // Use default values if loading fails
      _themeMode = ThemeMode.light;
      _isDarkMode = false;
      _useSystemTheme = true;
      _useHighContrast = false;
      _useLargeText = false;
      _useReducedMotion = false;
      _fontScale = 1.0;
      _accentColor = AppTheme.accentColor;
      _fontFamily = AppTheme.defaultFontFamily;
    }
  }

  // Save theme preferences
  Future<void> _saveThemePreferences() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      
      await prefs.setBool(AppConstants.useSystemThemeKey, _useSystemTheme);
      await prefs.setBool(AppConstants.useHighContrastKey, _useHighContrast);
      await prefs.setBool(AppConstants.useLargeTextKey, _useLargeText);
      await prefs.setBool(AppConstants.useReducedMotionKey, _useReducedMotion);
      await prefs.setDouble(AppConstants.fontScaleKey, _fontScale);
      await prefs.setInt(AppConstants.accentColorKey, _accentColor.value);
      await prefs.setString(AppConstants.fontFamilyKey, _fontFamily);
      
      String themeModeString;
      switch (_themeMode) {
        case ThemeMode.light:
          themeModeString = 'light';
          break;
        case ThemeMode.dark:
          themeModeString = 'dark';
          break;
        case ThemeMode.system:
          themeModeString = 'system';
          break;
      }
      await prefs.setString(AppConstants.themeModeKey, themeModeString);
    } catch (e) {
      // Ignore save errors
    }
  }

  // Get system theme mode
  ThemeMode _getSystemThemeMode() {
    final brightness = WidgetsBinding.instance.platformDispatcher.platformBrightness;
    return brightness == Brightness.dark ? ThemeMode.dark : ThemeMode.light;
  }

  // Apply theme
  void _applyTheme() {
    if (_useSystemTheme) {
      _themeMode = ThemeMode.system;
      _isDarkMode = _getSystemThemeMode() == ThemeMode.dark;
    }
    
    notifyListeners();
  }

  // Set light theme
  Future<void> setLightTheme() async {
    _themeMode = ThemeMode.light;
    _isDarkMode = false;
    _useSystemTheme = false;
    
    await _saveThemePreferences();
    notifyListeners();
  }

  // Set dark theme
  Future<void> setDarkTheme() async {
    _themeMode = ThemeMode.dark;
    _isDarkMode = true;
    _useSystemTheme = false;
    
    await _saveThemePreferences();
    notifyListeners();
  }

  // Set system theme
  Future<void> setSystemTheme() async {
    _themeMode = ThemeMode.system;
    _useSystemTheme = true;
    _isDarkMode = _getSystemThemeMode() == ThemeMode.dark;
    
    await _saveThemePreferences();
    notifyListeners();
  }

  // Toggle theme
  Future<void> toggleTheme() async {
    if (_isDarkMode) {
      await setLightTheme();
    } else {
      await setDarkTheme();
    }
  }

  // Toggle high contrast
  Future<void> toggleHighContrast() async {
    _useHighContrast = !_useHighContrast;
    await _saveThemePreferences();
    notifyListeners();
  }

  // Toggle large text
  Future<void> toggleLargeText() async {
    _useLargeText = !_useLargeText;
    await _saveThemePreferences();
    notifyListeners();
  }

  // Toggle reduced motion
  Future<void> toggleReducedMotion() async {
    _useReducedMotion = !_useReducedMotion;
    await _saveThemePreferences();
    notifyListeners();
  }

  // Set font scale
  Future<void> setFontScale(double scale) async {
    if (scale < 0.5 || scale > 3.0) return;
    
    _fontScale = scale;
    await _saveThemePreferences();
    notifyListeners();
  }

  // Set accent color
  Future<void> setAccentColor(Color color) async {
    _accentColor = color;
    await _saveThemePreferences();
    notifyListeners();
  }

  // Set font family
  Future<void> setFontFamily(String fontFamily) async {
    if (!AppTheme.availableFonts.contains(fontFamily)) return;
    
    _fontFamily = fontFamily;
    await _saveThemePreferences();
    notifyListeners();
  }

  // Reset to defaults
  Future<void> resetToDefaults() async {
    _themeMode = ThemeMode.light;
    _isDarkMode = false;
    _useSystemTheme = true;
    _useHighContrast = false;
    _useLargeText = false;
    _useReducedMotion = false;
    _fontScale = 1.0;
    _accentColor = AppTheme.accentColor;
    _fontFamily = AppTheme.defaultFontFamily;
    
    await _saveThemePreferences();
    notifyListeners();
  }

  // Get current theme data
  ThemeData getCurrentTheme() {
    final baseTheme = _isDarkMode ? AppTheme.darkTheme : AppTheme.lightTheme;
    
    return baseTheme.copyWith(
      colorScheme: baseTheme.colorScheme.copyWith(
        primary: _accentColor,
        secondary: _accentColor,
      ),
      textTheme: baseTheme.textTheme.apply(
        fontFamily: _fontFamily,
        fontSizeFactor: _fontScale,
      ),
      primaryTextTheme: baseTheme.primaryTextTheme.apply(
        fontFamily: _fontFamily,
        fontSizeFactor: _fontScale,
      ),
      inputDecorationTheme: baseTheme.inputDecorationTheme.copyWith(
        labelStyle: baseTheme.inputDecorationTheme.labelStyle?.copyWith(
          fontFamily: _fontFamily,
          fontSize: baseTheme.inputDecorationTheme.labelStyle!.fontSize! * _fontScale,
        ),
        hintStyle: baseTheme.inputDecorationTheme.hintStyle?.copyWith(
          fontFamily: _fontFamily,
          fontSize: baseTheme.inputDecorationTheme.hintStyle!.fontSize! * _fontScale,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: baseTheme.elevatedButtonTheme.style?.copyWith(
          textStyle: baseTheme.elevatedButtonTheme.style?.textStyle?.copyWith(
            fontFamily: _fontFamily,
            fontSize: baseTheme.elevatedButtonTheme.style?.textStyle?.fontSize! * _fontScale,
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: baseTheme.outlinedButtonTheme.style?.copyWith(
          textStyle: baseTheme.outlinedButtonTheme.style?.textStyle?.copyWith(
            fontFamily: _fontFamily,
            fontSize: baseTheme.outlinedButtonTheme.style?.textStyle?.fontSize! * _fontScale,
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: baseTheme.textButtonTheme.style?.copyWith(
          textStyle: baseTheme.textButtonTheme.style?.textStyle?.copyWith(
            fontFamily: _fontFamily,
            fontSize: baseTheme.textButtonTheme.style?.textStyle?.fontSize! * _fontScale,
          ),
        ),
      ),
    );
  }

  // Get high contrast theme
  ThemeData getHighContrastTheme() {
    final baseTheme = getCurrentTheme();
    
    if (!_useHighContrast) return baseTheme;
    
    return baseTheme.copyWith(
      colorScheme: baseTheme.colorScheme.copyWith(
        primary: Colors.white,
        onPrimary: Colors.black,
        secondary: Colors.yellow,
        onSecondary: Colors.black,
        surface: Colors.black,
        onSurface: Colors.white,
        background: Colors.black,
        onBackground: Colors.white,
        error: Colors.red,
        onError: Colors.white,
      ),
      cardTheme: baseTheme.cardTheme.copyWith(
        color: Colors.black,
        shadowColor: Colors.white,
      ),
      appBarTheme: baseTheme.appBarTheme.copyWith(
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        elevation: 4,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: baseTheme.elevatedButtonTheme.style?.copyWith(
          backgroundColor: MaterialStateProperty.all(Colors.white),
          foregroundColor: MaterialStateProperty.all(Colors.black),
          side: MaterialStateProperty.all(const BorderSide(color: Colors.white, width: 2)),
        ),
      ),
    );
  }

  // Get large text theme
  ThemeData getLargeTextTheme() {
    final baseTheme = _useHighContrast ? getHighContrastTheme() : getCurrentTheme();
    
    if (!_useLargeText) return baseTheme;
    
    return baseTheme.copyWith(
      textTheme: baseTheme.textTheme.apply(
        fontSizeFactor: 1.3,
      ),
      primaryTextTheme: baseTheme.primaryTextTheme.apply(
        fontSizeFactor: 1.3,
      ),
      inputDecorationTheme: baseTheme.inputDecorationTheme.copyWith(
        labelStyle: baseTheme.inputDecorationTheme.labelStyle?.copyWith(
          fontSize: baseTheme.inputDecorationTheme.labelStyle!.fontSize! * 1.3,
        ),
        hintStyle: baseTheme.inputDecorationTheme.hintStyle?.copyWith(
          fontSize: baseTheme.inputDecorationTheme.hintStyle!.fontSize! * 1.3,
        ),
      ),
    );
  }

  // Get final theme
  ThemeData getTheme() {
    return getLargeTextTheme();
  }

  // Check if theme is accessible
  bool get isAccessible {
    return _useHighContrast || _useLargeText || _fontScale > 1.0;
  }

  // Get theme info
  Map<String, dynamic> getThemeInfo() {
    return {
      'themeMode': _themeMode.toString(),
      'isDarkMode': _isDarkMode,
      'useSystemTheme': _useSystemTheme,
      'useHighContrast': _useHighContrast,
      'useLargeText': _useLargeText,
      'useReducedMotion': _useReducedMotion,
      'fontScale': _fontScale,
      'accentColor': _accentColor.value,
      'fontFamily': _fontFamily,
      'isAccessible': isAccessible,
    };
  }

  // Get available themes
  List<Map<String, dynamic>> getAvailableThemes() {
    return [
      {
        'name': 'Light',
        'description': 'Clean and bright theme',
        'icon': Icons.light_mode,
        'themeMode': ThemeMode.light,
      },
      {
        'name': 'Dark',
        'description': 'Easy on the eyes',
        'icon': Icons.dark_mode,
        'themeMode': ThemeMode.dark,
      },
      {
        'name': 'System',
        'description': 'Follows device settings',
        'icon': Icons.settings_system_daydream,
        'themeMode': ThemeMode.system,
      },
    ];
  }

  // Get available accent colors
  List<Map<String, dynamic>> getAvailableAccentColors() {
    return [
      {
        'name': 'Blue',
        'color': AppTheme.accentColor,
        'description': 'Default accent color',
      },
      {
        'name': 'Green',
        'color': AppTheme.successColor,
        'description': 'Success and positive actions',
      },
      {
        'name': 'Orange',
        'color': AppTheme.warningColor,
        'description': 'Warning and attention',
      },
      {
        'name': 'Purple',
        'color': Colors.purple,
        'description': 'Creative and innovative',
      },
      {
        'name': 'Teal',
        'color': Colors.teal,
        'description': 'Professional and calm',
      },
    ];
  }

  // Get available font families
  List<Map<String, dynamic>> getAvailableFonts() {
    return [
      {
        'name': 'Poppins',
        'family': 'Poppins',
        'description': 'Modern and readable',
      },
      {
        'name': 'Roboto',
        'family': 'Roboto',
        'description': 'Clean and professional',
      },
      {
        'name': 'Open Sans',
        'family': 'OpenSans',
        'description': 'Friendly and approachable',
      },
      {
        'name': 'Lato',
        'family': 'Lato',
        'description': 'Warm and friendly',
      },
      {
        'name': 'Source Sans Pro',
        'family': 'SourceSansPro',
        'description': 'Legible and versatile',
      },
    ];
  }

  // Check if theme supports accessibility
  bool supportsAccessibility() {
    return true; // All themes support accessibility features
  }

  // Get accessibility recommendations
  List<String> getAccessibilityRecommendations() {
    final recommendations = <String>[];
    
    if (!_useHighContrast) {
      recommendations.add('Enable high contrast for better visibility');
    }
    
    if (!_useLargeText) {
      recommendations.add('Enable large text for better readability');
    }
    
    if (_fontScale < 1.2) {
      recommendations.add('Increase font size for better readability');
    }
    
    if (!_useReducedMotion) {
      recommendations.add('Enable reduced motion if you\'re sensitive to animations');
    }
    
    return recommendations;
  }
}

