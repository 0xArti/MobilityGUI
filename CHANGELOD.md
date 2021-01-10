# Changelog

## 0.2
What's New
* Added service for linux using Supervisor (in progress)
* Added settings.json\
    General settings for the app:\
    __Popup_timeout__: Time in minutes before popup appears or updates\
    __Idle_timeout__: User AFK minutes to stop the _popup_timeout_ timer\
    __Equipment__: Global setting if the user has any equipment available\
    __Template__: The logic to call when generating exercises
* Added equipment\
    The available equipment is:
    * Bar (e.g. Pull up bar)
    * Stick (e.g. Broomstick)
    * Massage Ball (e.g. Lacrosse Ball)
    * Light Weights (e.g. 0.5kg - 2.5kg)
    * Rings (e.g. Gymnastic Rings)
    * Resistance Bands 
* Added more exercises and types
* Added guide for exercises\
    The Guide can be view under docs/guide
* Added templates

Bug Fixes
* Repetition does no changed for the same exercise
* When user AFK, the popup timer still run
* DynamicConfig is now case-insensitive

---

## 0.1
* Initial Publish