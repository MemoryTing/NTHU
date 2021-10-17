#include <stdio.h>
#include <allegro5/allegro.h>
#include <allegro5/allegro_primitives.h>
#include <allegro5/allegro_image.h>
#include <allegro5/allegro_audio.h>
#include <allegro5/allegro_acodec.h>
#include <allegro5/allegro_font.h>
#include <allegro5/allegro_ttf.h>

#define GAME_TERMINATE -1

// ALLEGRO Variables
ALLEGRO_DISPLAY* display = NULL;
ALLEGRO_EVENT_QUEUE *event_queue = NULL;
ALLEGRO_BITMAP *image = NULL;
ALLEGRO_BITMAP *image2 = NULL;
ALLEGRO_BITMAP *image3 = NULL;
ALLEGRO_BITMAP *background = NULL;
ALLEGRO_BITMAP *background1 = NULL;
ALLEGRO_BITMAP *background2 = NULL;
ALLEGRO_KEYBOARD_STATE keyState ;
ALLEGRO_TIMER *timer = NULL;
ALLEGRO_TIMER *timer2 = NULL;
ALLEGRO_SAMPLE *song=NULL;
ALLEGRO_FONT *font = NULL;

//Custom Definition
const char *title = "Final Project 106062122";
const float FPS = 60;
const int WIDTH = 1000;
const int HEIGHT = 600;
typedef struct character
{
    int x;
    int y;
    int blood;
    ALLEGRO_BITMAP *image_path;

}Character;

Character character1;
Character character2;
Character character3;
Character character4;
Character character5;
Character character6;
Character character7;
Character character8;
Character character9;
Character character1_photo , character1_photo2;
Character character2_photo , character2_photo2;
Character start1 , start2;
Character exit1 , exit2;
Character about1 , about2;
Character blood_s , blood1_s , blood2_s , blood3_s , blood4_s , blood5_s , blood6_s , blood7_s , blood8_s , blood9_s , blood10_s;
Character blood_c , blood1_c , blood2_c , blood3_c , blood4_c , blood5_c , blood6_c , blood7_c , blood8_c , blood9_c , blood10_c;
Character c_win , s_win;
Character exit3 , restart;
Character back1 , back2;
int smove , cmove;
int mouse;

int imageWidth = 0;
int imageHeight = 0;
int draw = 0;
int done = 0;
int window = 1;
bool judge_next_window = false;
bool ture_1 , ture_2;
bool judge_next_window_2 = false;

void show_err_msg(int msg);
void game_init();
void game_begin();
int process_event();
int game_run();
void game_destroy();

int main(int argc, char *argv[]) {
    int msg = 0;

    game_init();
    game_begin();

    while (msg != GAME_TERMINATE) {
        msg = game_run();
        if (msg == GAME_TERMINATE)
            printf("Game Over\n");
    }

    game_destroy();
    return 0;
}

void show_err_msg(int msg) {
    fprintf(stderr, "unexpected msg: %d\n", msg);
    game_destroy();
    exit(9);
}

void game_init() {
    if (!al_init()) {
        show_err_msg(-1);
    }
    if(!al_install_audio()){
        fprintf(stderr, "failed to initialize audio!\n");
        show_err_msg(-1);
    }
    if(!al_init_acodec_addon()){
        fprintf(stderr, "failed to initialize audio codecs!\n");
        show_err_msg(-1);
    }
    if (!al_reserve_samples(1)){
        fprintf(stderr, "failed to reserve samples!\n");
        show_err_msg(-1);
    }
    // Create display
    display = al_create_display(WIDTH, HEIGHT);
    event_queue = al_create_event_queue();
    if (display == NULL || event_queue == NULL) {
        show_err_msg(-1);
    }
    // Initialize Allegro settings
    al_set_window_position(display, 0, 0);
    al_set_window_title(display, title);
    al_init_primitives_addon();
    al_install_keyboard();
    al_install_audio();
    al_init_image_addon();
    al_init_acodec_addon();
    al_init_font_addon();
    al_init_ttf_addon();
    al_init_primitives_addon();
    al_install_mouse();

    // Register event
    al_register_event_source(event_queue, al_get_display_event_source(display));
    al_register_event_source(event_queue, al_get_keyboard_event_source());
    al_register_event_source(event_queue, al_get_mouse_event_source());
    al_get_display_event_source(display);

    //load
    about1.image_path = al_load_bitmap("about1.png");
    about2.image_path = al_load_bitmap("about2.png");
    exit1.image_path= al_load_bitmap("exit1.png");
    exit2.image_path = al_load_bitmap("exit2.png");
    exit3.image_path = al_load_bitmap("exit.png");
    start1.image_path = al_load_bitmap("start1.png");
    start2.image_path = al_load_bitmap("start2.png");
    back1.image_path = al_load_bitmap("back2.png");
    back2.image_path = al_load_bitmap("back.png");
    background = al_load_bitmap("background.jpg");
    background1 = al_load_bitmap("background1.png");
    background2 = al_load_bitmap("background2.png");
    character1.image_path = al_load_bitmap("Charmander.png");
    character2.image_path= al_load_bitmap("Squirtle.png");
    character3.image_path = al_load_bitmap("Squirtle2.png");
    character4.image_path = al_load_bitmap("charmander2.png");
    character5.image_path = al_load_bitmap("charmander_attack.png");
    character6.image_path = al_load_bitmap("Charmander_lose.png");
    character7.image_path = al_load_bitmap("Squirtle_lose.png");
    character8.image_path = al_load_bitmap("Charmander_win.png");
    character9.image_path = al_load_bitmap("Squirtle_win.png");
    character1_photo.image_path = al_load_bitmap("Charmander_photo.png");
    character1_photo2.image_path = al_load_bitmap("Charmander_photo2.png");
    character2_photo.image_path = al_load_bitmap("Squirtle_photo.png");
    character2_photo2.image_path = al_load_bitmap("Squirtle_photo2.png");
    blood_c.image_path = al_load_bitmap("blood.png");
    blood1_c.image_path = al_load_bitmap("blood1_c.png");
    blood2_c.image_path = al_load_bitmap("blood2_c.png");
    blood3_c.image_path = al_load_bitmap("blood3_c.png");
    blood4_c.image_path = al_load_bitmap("blood4_c.png");
    blood5_c.image_path = al_load_bitmap("blood5_c.png");
    blood6_c.image_path = al_load_bitmap("blood6_c.png");
    blood7_c.image_path = al_load_bitmap("blood7_c.png");
    blood8_c.image_path = al_load_bitmap("blood8_c.png");
    blood9_c.image_path = al_load_bitmap("blood9_c.png");
    blood10_c.image_path = al_load_bitmap("blood10.png");
    blood_s.image_path = al_load_bitmap("blood.png");
    blood1_s.image_path = al_load_bitmap("blood1_s.png");
    blood2_s.image_path = al_load_bitmap("blood2_s.png");
    blood3_s.image_path = al_load_bitmap("blood3_s.png");
    blood4_s.image_path = al_load_bitmap("blood4_s.png");
    blood5_s.image_path = al_load_bitmap("blood5_s.png");
    blood6_s.image_path = al_load_bitmap("blood6_s.png");
    blood7_s.image_path = al_load_bitmap("blood7_s.png");
    blood8_s.image_path = al_load_bitmap("blood8_s.png");
    blood9_s.image_path = al_load_bitmap("blood9_s.png");
    blood10_s.image_path = al_load_bitmap("blood10.png");
    s_win.image_path = al_load_bitmap("Squirtle WIN.png");
    c_win.image_path = al_load_bitmap("Charmander WIN.png");
    restart.image_path = al_load_bitmap("restart.png");

}

void game_begin() {
    // Load sound
    /*song = al_load_sample( "jump.wav" );
    if (!song){
        printf( "Audio clip sample not loaded!\n" );
        show_err_msg(-1);
    }
    // Loop the song until the display closes
    al_play_sample(song, 1.0, 0.0,1.0,ALLEGRO_PLAYMODE_LOOP,NULL);
    al_clear_to_color(al_map_rgb(0,0,0));*/
    // Load and draw text
    about1.x = WIDTH / 2 - 470;
    about1.y = HEIGHT / 2;
    exit1.x = WIDTH / 2 + 150;
    exit1.y = HEIGHT / 2;
    start1.x = WIDTH/2 - 170;
    start1.y = HEIGHT/2;
    al_draw_bitmap(about1.image_path, about1.x, about1.y, 0);
    al_draw_bitmap(exit1.image_path, exit1.x, exit1.y, 0);
    al_draw_bitmap(start1.image_path, start1.x, start1.y, 0);
    al_draw_bitmap(background1 , 12 , 12 , 0);
    al_flip_display();
}

int process_event(){
    // Request the event
    ALLEGRO_EVENT event;
    al_wait_for_event(event_queue, &event);

    // Our setting for controlling animation
    if(event.timer.source == timer){
        ture_1 = !ture_1 ;
    }
    if(event.timer.source == timer2){
        ture_2 = !ture_2 ;
    }

    // Keyboard
    if (character1.blood > 0 && character2.blood > 0 && event.type == ALLEGRO_EVENT_KEY_UP){
        switch(event.keyboard.keycode)
        {
            // P1 control
            case ALLEGRO_KEY_Z:
                if (character1.x - 30 > 0 && character1.x - 30 <= WIDTH-200) {
                    character1.x -= 30;
                    if (character1.x+50 == character2.x) character2.blood -= 1;
                }
                break;

            case ALLEGRO_KEY_C:
                if (character1.x + 30 > 0 && character1.x + 30 <= WIDTH-200) {
                    character1.x += 30;
                    if (character1.x+50 == character2.x && character2.y - 50 == character1.y) character2.blood -= 1;
                }
                break;
            case ALLEGRO_KEY_S:
                if (character1 .x + 90 > 0 && character1.x + 90 <= WIDTH-175) {
                    character1.x += 90;
                    if (character1.x >= character2.x-10 && character1.x <= character2.x+150) {
                        character2.blood -= 1;
                    }
                }
                break;
            case ALLEGRO_KEY_X:
                if (character1.x - 90 > 0 && character1.x - 90 <= WIDTH-175) {
                    character1.x -= 90;
                    if (character1.x >= character2.x-10 && character1.x <= character2.x+150) {
                        character2.blood -= 1;
                    }
                }
                break;
        }
    }
    switch(event.keyboard.keycode)
    {

        // P2 control
        case ALLEGRO_KEY_RIGHT:
            if (character1.blood > 0 && character2.blood > 0){
                if (character2.x + 30 > 0 && character2.x + 30 <= WIDTH-175) {
                    character2.x += 30;
                    if (character2.x-50 == character1.x) character1.blood -= 1;
                }
                break;
            }
        case ALLEGRO_KEY_LEFT:
            if (character1.blood > 0 && character2.blood > 0){
                if (character2.x - 30 > 0 && character2.x - 30 <= WIDTH-175) {
                    character2.x -= 30;
                    if (character2.x-50 == character1.x) character1.blood -= 1;
                }
                break;
            }

        // For Start Menu
        case ALLEGRO_KEY_ENTER:
            judge_next_window = true;
            break;
        case ALLEGRO_KEY_E:
            return GAME_TERMINATE;
        case ALLEGRO_KEY_T:
            judge_next_window_2 = true;
            break;
        case ALLEGRO_KEY_R:
            window = 1;
            judge_next_window = true;
            break;
    }

    if (character1.blood > 0 && character2.blood > 0 && event.type == ALLEGRO_EVENT_KEY_UP){
        switch(event.keyboard.keycode){
            case ALLEGRO_KEY_UP:
                character2.y += 250;
                break;
            case ALLEGRO_KEY_ALT:
                character5.blood = 0;
                break;
        }
    }
    else if (character1.blood > 0 && character2.blood > 0 && event.type == ALLEGRO_EVENT_KEY_DOWN){
        switch(event.keyboard.keycode){
            case ALLEGRO_KEY_UP:
                character2.y -= 250;
                if (character2.y+200 == character1.y && character2.x >= character1.x-50 && character2.x <= character1.x+200) {
                    character1.blood -= 1;
                }
                break;
            case ALLEGRO_KEY_ALT:
                character5.blood = 1;
                if (character2.x >= character1.x+310 && character2.x <= character1.x+590 && character1.y <= character2.y) character2.blood-=2;
                break;
        }
    }
    else if (event.type == ALLEGRO_EVENT_MOUSE_AXES){
        int x = event.mouse.x;
        int y = event.mouse.y;
        if (window == 1 && x >= about1.x && x <= about1.x+350 && y >= about1.y && y <= about1.y+350){
            al_draw_bitmap(about2.image_path, about1.x, about1.y-150, 0);
            al_flip_display();
        }
        else if (window == 1 && x >= start1.x && x <= start1.x+350 && y >= start1.y && y <= start1.y+350){
            al_draw_bitmap(start2.image_path, start1.x, start1.y-150, 0);
            al_flip_display();
        }
        else if (window == 1 && x >= exit1.x && x <= exit1.x+350 && y >= exit1.y && y <= exit1.y+350){
            al_draw_bitmap(exit2.image_path, exit1.x, exit1.y-150, 0);
            al_flip_display();
        }
        else if (window == 3 && x >= back1.x && x <= back1.x+150 && y >= back1.y && y <= back1.y+100){
            back2.blood = 1;
        }
        else if (x <= back1.x || x >= back1.x+150 || y <= back1.y || y >= back1.y+100){
            back2.blood = 0;
        }
    }

    else if (event.type == ALLEGRO_EVENT_MOUSE_BUTTON_DOWN){
        if (event.mouse.button == 1){
            window = 1;
            }
        }
        else if (event.type == ALLEGRO_EVENT_MOUSE_BUTTON_UP){
            al_clear_to_color(al_map_rgb(0,0,0));
            al_draw_bitmap(about1.image_path, about1.x, about1.y, 0);
            al_draw_bitmap(exit1.image_path, exit1.x, exit1.y, 0);
            al_draw_bitmap(start1.image_path, start1.x, start1.y, 0);
            al_draw_bitmap(background1 , 12 , 12 , 0);
            al_flip_display();
        }

    // Shutdown our program
    else if(event.type == ALLEGRO_EVENT_DISPLAY_CLOSE)
        return GAME_TERMINATE;

    return 0;
}

int game_run() {
    int error = 0;
    // First window(Menu)
    if(window == 1){
        if (!al_is_event_queue_empty(event_queue)) {
            error = process_event();
            if(judge_next_window) {
                judge_next_window = false;
                window = 2;
                // Setting Character
                character1.x = WIDTH / 2 - 300;
                character1.y = HEIGHT / 2 - 50;
                character2.x = WIDTH / 2 + 170;
                character2.y = HEIGHT / 2 ;
                character1.blood = 10;
                character2.blood = 10;
                character5.blood = 0;

                //Initialize Timer
                timer  = al_create_timer(1.0);
                timer2  = al_create_timer(1.0/3.0);
                al_register_event_source(event_queue, al_get_timer_event_source(timer)) ;
                al_register_event_source(event_queue, al_get_timer_event_source(timer2)) ;
                al_start_timer(timer);
                al_start_timer(timer2);
            }
            else if (judge_next_window_2){
                judge_next_window_2 = false;
                window = 3;
                back1.x = WIDTH - 200;
                back1.y = 20;
            }
        }
    }
    // Second window(Main Game)
    else if(window == 2){
        // Change Image for animation
        al_draw_bitmap(background, 0,0, 0);
        if (character1.blood <= 0)al_draw_bitmap(character6.image_path, WIDTH / 2 + 200, HEIGHT / 2 + 50, 0);
        else if (character2.blood <= 0)al_draw_bitmap(character8.image_path , WIDTH / 2 - 300 , HEIGHT / 2 - 300 , 0);
        else if (character5.blood == 1)al_draw_bitmap(character5.image_path, character1.x, character1.y, 0);
        else if(ture_1)al_draw_bitmap(character1.image_path, character1.x, character1.y, 0);
        else al_draw_bitmap(character4.image_path, character1.x-3, character1.y-3, 0);
        if (character2.blood <= 0)al_draw_bitmap(character7.image_path, WIDTH / 2 + 170, HEIGHT / 2, 0);
        else if (character1.blood <= 0)al_draw_bitmap(character9.image_path , WIDTH / 2 - 300 , HEIGHT / 2 - 250 , 0);
        else if(ture_2)al_draw_bitmap(character3.image_path, character2.x, character2.y, 0);
        else al_draw_bitmap(character2.image_path, character2.x, character2.y, 0);
        if (character1.blood > 5)al_draw_bitmap(character1_photo.image_path , 10 , 10 , 0);
        else al_draw_bitmap(character1_photo2 .image_path , 10 , 10 , 0);
        if (character2.blood > 5)al_draw_bitmap(character2_photo.image_path , 940 , 10 , 0);
        else al_draw_bitmap(character2_photo2.image_path , 940 , 10 , 0);
        if (character1.blood == 10)al_draw_bitmap(blood_c.image_path , 70 , 15 , 0);
        else if (character1.blood == 9){
            al_draw_bitmap(blood1_c.image_path , 70 , 15 , 0);
        }
        else if (character1.blood == 8){
            al_draw_bitmap(blood2_c.image_path , 70 , 15 , 0);
        }
        else if (character1.blood == 7){
            al_draw_bitmap(blood3_c.image_path , 70 , 15 , 0);
        }
        else if (character1.blood == 6){
            al_draw_bitmap(blood4_c.image_path , 70 , 15 , 0);
        }
        else if (character1.blood == 5){
            al_draw_bitmap(blood5_c.image_path , 70 , 15 , 0);
        }
        else if (character1.blood == 4){
            al_draw_bitmap(blood6_c.image_path , 70 , 15 , 0);
        }
        else if (character1.blood == 3){
            al_draw_bitmap(blood7_c.image_path , 70 , 15 , 0);
        }
        else if (character1.blood == 2){
            al_draw_bitmap(blood8_c.image_path , 70 , 15 , 0);
        }
        else if (character1.blood == 1){
            al_draw_bitmap(blood9_c.image_path , 70 , 15 , 0);
        }
        else {
            al_draw_bitmap(blood10_c.image_path , 70 , 15 , 0);
            al_draw_bitmap(s_win.image_path , 20 , 100 , 0);
            al_draw_bitmap(restart.image_path , 45 , 532 , 0);
            al_draw_bitmap(exit3.image_path , 750 , 532 , 0);
        }

        if (character2.blood == 10)al_draw_bitmap(blood_s.image_path , WIDTH/2 + 80 , 15 , 0);
        else if (character2.blood == 9){
            al_draw_bitmap(blood1_s.image_path , WIDTH/2 + 80 , 15 , 0);
        }
        else if (character2.blood == 8){
            al_draw_bitmap(blood2_s.image_path , WIDTH/2 + 80 , 15 , 0);
        }
        else if (character2.blood == 7){
            al_draw_bitmap(blood3_s.image_path , WIDTH/2 + 80 , 15 , 0);
        }
        else if (character2.blood == 6){
            al_draw_bitmap(blood4_s.image_path , WIDTH/2 + 80 , 15 , 0);
        }
        else if (character2.blood == 5){
            al_draw_bitmap(blood5_s.image_path , WIDTH/2 + 80 , 15 , 0);
        }
        else if (character2.blood == 4){
            al_draw_bitmap(blood6_s.image_path , WIDTH/2 + 80 , 15 , 0);
        }
        else if (character2.blood == 3){
            al_draw_bitmap(blood7_s.image_path , WIDTH/2 + 80 , 15 , 0);
        }
        else if (character2.blood == 2){
            al_draw_bitmap(blood8_s.image_path , WIDTH/2 + 80 , 15 , 0);
        }
        else if (character2.blood == 1){
            al_draw_bitmap(blood9_s.image_path , WIDTH/2 + 80 , 15 , 0);
        }
        else {
            al_draw_bitmap(blood10_s.image_path , WIDTH/2 + 80 , 15 , 0);
            al_draw_bitmap(c_win.image_path , 20 , 100 , 0);
            al_draw_bitmap(restart.image_path , 45 , 532 , 0);
            al_draw_bitmap(exit3.image_path , 750 , 532 , 0);
        }

        al_flip_display();
        al_clear_to_color(al_map_rgb(0,0,0));

        // Listening for new event
        if (!al_is_event_queue_empty(event_queue)) {
            error = process_event();
        }
    }
    else if (window == 3){
        al_draw_bitmap(background2 , 0 , 0 , 0);
        if (back2.blood != 1)al_draw_bitmap(back1.image_path , back1.x , back1.y , 0);
        else {
            al_draw_bitmap(back2.image_path , back1.x , back1.y , 0);
        }
        al_flip_display();

        if (!al_is_event_queue_empty(event_queue)) {
            error = process_event();
        }
    }

    return error;
}

void game_destroy() {
    // Make sure you destroy all things
    al_destroy_event_queue(event_queue);
    al_destroy_display(display);
    al_destroy_timer(timer);
    al_destroy_timer(timer2);
    al_destroy_bitmap(image);
    al_destroy_sample(song);
}
