/**
 * @file dbrobot_emoji_gif.c
 * @brief DB_robot GIF emoji component - minimal API, content is gifs/ folder
 * only
 */

#include "dbrobot_emoji_gif.h"
#include <stddef.h>

#ifndef DBROBOT_EMOJI_GIF_VERSION
#define DBROBOT_EMOJI_GIF_VERSION "1.1.1"
#endif

static const char *const gif_names[] = {
    "staticstate", "sad", "happy", "scare", "buxue", "anger", NULL};

const char *dbrobot_emoji_gif_get_version(void) { return DBROBOT_EMOJI_GIF_VERSION; }

int dbrobot_emoji_gif_get_count(void) { return 6; }

const char *dbrobot_emoji_gif_get_name(int index) {
  if (index < 0 || index >= 6) {
    return NULL;
  }
  return gif_names[index];
}
