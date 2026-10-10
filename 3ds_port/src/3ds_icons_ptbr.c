/*
 * The Portuguese build's graphics with English words, redrawn when they are
 * read from the data pack (ReadPayload, 3ds_assets.c): the player's own
 * sheet keeps its frames and colours, its English letters are cleared and
 * the Portuguese name is written in a small capital font drawn for this
 * project. No pixel of the game is kept here.
 *
 * tools/type_icons_ptbr.py draws the same thing into a PNG, as a preview.
 */
#include <string.h>

/* Declared in compat/port_platform.h, which 3ds_assets.c includes. */
void Port_TransformAsset(const char *path, unsigned char *data, unsigned size);

#if defined(CTR_LANG_PT_BR)

/* 4bpp tiles, 16 to a row: graphics/interface/menu_info.4bpp is 128x128. */
#define SHEET_TILES_WIDE 16
#define INK 0xF
#define SHADOW 0xE

static unsigned SheetPixel(const unsigned char *tiles, int x, int y)
{
    const unsigned char *tile = tiles + ((y / 8) * SHEET_TILES_WIDE + x / 8) * 32;
    unsigned char byte = tile[(y % 8) * 4 + (x % 8) / 2];
    return (x & 1) ? byte >> 4 : byte & 0xF;
}

static void SetSheetPixel(unsigned char *tiles, int x, int y, unsigned value)
{
    unsigned char *tile = tiles + ((y / 8) * SHEET_TILES_WIDE + x / 8) * 32;
    unsigned char *byte = &tile[(y % 8) * 4 + (x % 8) / 2];
    *byte = (x & 1) ? (unsigned char)((*byte & 0x0F) | (value << 4)) : (unsigned char)((*byte & 0xF0) | value);
}

/*
 * A capital font 3 pixels wide (M 5, N 4) and 7 high, '#' for ink; the
 * accents sit on the row above. Drawn for this project.
 */
struct Glyph
{
    char ch;
    const char *rows[7];
};

static const struct Glyph sGlyphs[] = {
    {'A', {".#.", "#.#", "#.#", "###", "#.#", "#.#", "#.#"}},
    {'B', {"##.", "#.#", "#.#", "##.", "#.#", "#.#", "##."}},
    {'C', {".##", "#..", "#..", "#..", "#..", "#..", ".##"}},
    {'D', {"##.", "#.#", "#.#", "#.#", "#.#", "#.#", "##."}},
    {'E', {"###", "#..", "#..", "##.", "#..", "#..", "###"}},
    {'F', {"###", "#..", "#..", "##.", "#..", "#..", "#.."}},
    {'G', {".##", "#..", "#..", "#.#", "#.#", "#.#", ".##"}},
    {'H', {"#.#", "#.#", "#.#", "###", "#.#", "#.#", "#.#"}},
    {'I', {"###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"}},
    {'L', {"#..", "#..", "#..", "#..", "#..", "#..", "###"}},
    {'M', {"#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"}},
    {'N', {"#..#", "##.#", "##.#", "#.##", "#.##", "#..#", "#..#"}},
    {'O', {".#.", "#.#", "#.#", "#.#", "#.#", "#.#", ".#."}},
    {'P', {"##.", "#.#", "#.#", "##.", "#..", "#..", "#.."}},
    {'Q', {".#.", "#.#", "#.#", "#.#", "#.#", "##.", ".##"}},
    {'R', {"##.", "#.#", "#.#", "##.", "#.#", "#.#", "#.#"}},
    {'S', {".##", "#..", "#..", ".#.", "..#", "..#", "##."}},
    {'T', {"###", ".#.", ".#.", ".#.", ".#.", ".#.", ".#."}},
    {'U', {"#.#", "#.#", "#.#", "#.#", "#.#", "#.#", "###"}},
    {'V', {"#.#", "#.#", "#.#", "#.#", "#.#", ".#.", ".#."}},
    {'.', {".", ".", ".", ".", ".", ".", "#"}},
};

/* The names as byte strings: 'a' stands for Á, 'e' for É, 'i' for Í, 'c' for
 * Ç and '~' for Ã, so the table stays ASCII. */
static const struct
{
    unsigned short tile;
    const char *name;
} sTypeNames[] = {
    {0x20, "NORMAL"}, {0x64, "LUTADOR"}, {0x60, "VOADOR"}, {0x80, "VENENO"}, {0x48, "TERRA"},
    {0x44, "PEDRA"}, {0x6C, "INSETO"}, {0x68, "FANTAS"}, {0x88, "AcO"}, {0x24, "FOGO"},
    {0x28, "aGUA"}, {0x2C, "PLANTA"}, {0x40, "ELeTR."}, {0x84, "PSiQ."}, {0x4C, "GELO"},
    {0xA0, "DRAG~O"}, {0x8C, "SOMBR."},
};

/* Ink of letter ch on row r (-1 the accent row, 0-6 the letter, 7 the
 * cedilla's tail) at column c; its width in *width. */
static int GlyphInk(char ch, int r, int c, int *width)
{
    char base = ch;
    unsigned i;

    switch (ch)
    {
    case 'a': case '~': base = 'A'; break;
    case 'e': base = 'E'; break;
    case 'i': base = 'I'; break;
    case 'c': base = 'C'; break;
    }
    for (i = 0; i < sizeof(sGlyphs) / sizeof(sGlyphs[0]); i++)
    {
        if (sGlyphs[i].ch != base)
            continue;
        *width = (int)strlen(sGlyphs[i].rows[0]);
        if (r == -1)
        {
            if (ch == 'a' || ch == 'e' || ch == 'i')
                return c == 1;
            if (ch == '~')
                return 1;
            return 0;
        }
        if (r == 7)
            return ch == 'c' && c == 1;
        return sGlyphs[i].rows[r][c] == '#';
    }
    *width = 0;
    return 0;
}

static void DrawTypeName(unsigned char *tiles, unsigned tile, const char *name)
{
    int x0 = (int)(tile % SHEET_TILES_WIDE) * 8, y0 = (int)(tile / SHEET_TILES_WIDE) * 8;
    unsigned rowBg[12];
    int total = -1, x, y;
    const char *p;

    /* Some icons fade to a second colour at the bottom: each row is
     * cleared with its own background, read at the icon's right edge. */
    for (y = 0; y < 12; y++)
    {
        rowBg[y] = 0;
        for (x = 31; x > 0; x--)
        {
            unsigned v = SheetPixel(tiles, x0 + x, y0 + y);
            if (v != INK && v != SHADOW && v != 0)
            {
                rowBg[y] = v;
                break;
            }
        }
        for (x = 0; x < 32; x++)
        {
            unsigned v = SheetPixel(tiles, x0 + x, y0 + y);
            if (v == INK || v == SHADOW)
                SetSheetPixel(tiles, x0 + x, y0 + y, rowBg[y]);
        }
    }
    for (p = name; *p; p++)
    {
        int w;
        GlyphInk(*p, 0, 0, &w);
        total += w + 1;
    }
    x = x0 + (31 - total) / 2;
    for (p = name; *p; p++)
    {
        int w, r, c;
        GlyphInk(*p, 0, 0, &w);
        for (r = -1; r <= 7; r++)
        {
            for (c = 0; c < w; c++)
            {
                int dx, dy, ink;
                int dummy;
                ink = GlyphInk(*p, r, c, &dummy);
                if (!ink)
                    continue;
                y = y0 + 2 + r; /* row -1 on the icon's row 1, the letter on rows 2-8 */
                SetSheetPixel(tiles, x + c, y, INK);
                for (dy = 0; dy <= 1; dy++)
                    for (dx = 0; dx <= 1; dx++)
                    {
                        int sy = y + dy - y0;
                        if ((dx || dy) && sy < 12 && SheetPixel(tiles, x + c + dx, y + dy) == rowBg[sy])
                            SetSheetPixel(tiles, x + c + dx, y + dy, SHADOW);
                    }
            }
        }
        x += w + 1;
    }
}

static int EndsWith(const char *path, const char *suffix)
{
    size_t n = strlen(path), m = strlen(suffix);
    return n >= m && strcmp(path + n - m, suffix) == 0;
}

void Port_TransformAsset(const char *path, unsigned char *data, unsigned size)
{
    unsigned i;

    if (EndsWith(path, "interface/menu_info.4bpp") && size >= 128 * 128 / 2)
        for (i = 0; i < sizeof(sTypeNames) / sizeof(sTypeNames[0]); i++)
            DrawTypeName(data, sTypeNames[i].tile, sTypeNames[i].name);
}

#else

void Port_TransformAsset(const char *path, unsigned char *data, unsigned size)
{
    (void)path;
    (void)data;
    (void)size;
}

#endif
