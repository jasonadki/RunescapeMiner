import pythoncom, pyHook
import pandas as pd

def OnKeyboardEvent(event):
    if event.KeyID == 13:  # "Enter"
        global i, df
        df = df.append({'a':i}, ignore_index=True)
        i = i+1
    else:
        print(df)

# return True to pass the event to other handlers
    return True


if __name__ == '__main__':
    i = 0
    df = pd.DataFrame(columns = ['a'])
    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all keyboard events
    hm.KeyDown = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()