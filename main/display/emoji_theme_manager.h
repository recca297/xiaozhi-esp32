#pragma once

#include <cstddef>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>
#include "emoji_collection.h"

#define EMOJI_THEME_ID_DEFAULT 0
#define EMOJI_THEME_ID_DBROBOT 1

// Forward declaration
class Display;

// Structure for an individual emoji item
struct EmojiItem_t {
    const char* name;     // Emotion name (e.g. "happy", "sad", "neutral", "winking", etc.)
    const uint8_t* data;  // Pointer to raw binary image data (e.g. GIF in Flash)
    size_t size;          // Size of the binary data in bytes
};

// Structure for managing an entire emoji set (Multi-theme/Emoji Sets)
struct EmojiSet_t {
    uint8_t id;                   // Theme ID: 0 = default, 1 = dbrobot
    const char* name;             // "default", "dbrobot"
    const char* description;      // Human-readable description
    bool is_font_fallback;        // True if font-based fallback (Noto Emoji / Material Symbols)
    bool force_black_background;  // True if this emoji set requires a black background

    // Dedicated pointers to common emotion images (cười, buồn, nháy mắt, v.v.)
    const uint8_t* happy_data;
    size_t happy_size;

    const uint8_t* sad_data;
    size_t sad_size;

    const uint8_t* neutral_data;
    size_t neutral_size;

    const uint8_t* winking_data;
    size_t winking_size;

    const uint8_t* angry_data;
    size_t angry_size;

    const uint8_t* laughing_data;
    size_t laughing_size;

    const uint8_t* crying_data;
    size_t crying_size;

    const uint8_t* thinking_data;
    size_t thinking_size;

    const uint8_t* cool_data;
    size_t cool_size;

    const uint8_t* surprised_data;
    size_t surprised_size;

    // List of all emoji items in this set
    std::vector<EmojiItem_t> items;

    // Pre-constructed EmojiCollection for LVGL display integration
    std::shared_ptr<EmojiCollection> collection;
};

// Singleton Emoji Theme Manager
class EmojiThemeManager {
public:
    static EmojiThemeManager& GetInstance();

    void Init();
    bool SetTheme(uint8_t theme_id, bool save_to_nvs = true);
    void ApplyCurrentTheme();
    void ApplyToThemes();
    void SetDefaultThemeCollection(std::shared_ptr<EmojiCollection> collection);
    void RegisterDisplay(Display* display);

    uint8_t GetCurrentThemeId() const { return current_theme_id_; }
    const EmojiSet_t* GetCurrentTheme() const;
    const EmojiSet_t* GetTheme(uint8_t theme_id) const;
    size_t GetThemeCount() const { return themes_.size(); }

private:
    EmojiThemeManager();
    void InitDefaultTheme();
    void InitDbrobotTheme();

    uint8_t current_theme_id_ = EMOJI_THEME_ID_DBROBOT;
    std::vector<EmojiSet_t> themes_;
    Display* display_ = nullptr;
    bool initialized_ = false;
};

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Dynamic theme switching API
 * @param theme_id 0 = default (font/noto_emoji), 1 = dbrobot (animated GIFs)
 */
void set_emoji_theme(uint8_t theme_id);

/**
 * @brief Get the currently active emoji theme ID
 */
uint8_t get_emoji_theme(void);

/**
 * @brief Get theme name by ID
 */
const char* get_emoji_theme_name(uint8_t theme_id);

#ifdef __cplusplus
}
#endif
