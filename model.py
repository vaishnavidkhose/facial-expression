import cv2
from deepface import DeepFace

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)

cap.set(3, 640) # set video widht
cap.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cap.get(3)
minH = 0.1*cap.get(4)


if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened:
    raise IOError('cannot open webcam')

  #frame count to set a threshold

#logic for emotion regonization
#count to store repeatation of expression
smile_count = 0
pale_count = 0
worried_count = 0
anxious_count = 0
surprise_count = 0
angry_count = 0
other_count = 0

#emotiones recognized by model 
emotions = ["happy", "sad", "neutral","fear","surprise","disgust","angry"]
frame_cnt = 1
#video capture and tracing
while True :
    frame_cnt = frame_cnt + 1
    ret, frame = cap.read()
    if ret== True :            
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
    

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 4)

        font = cv2.FONT_HERSHEY_SIMPLEX
        dom_emot = result['dominant_emotion']
        if dom_emot == 'happy' :
            expression = 'smile'
        elif dom_emot == 'sad' :
            expression = 'upset' 
        elif dom_emot == 'neutral' :
            expression = 'no expression'
        elif dom_emot == 'fear' :
            expression = 'anxious' 
        elif dom_emot == 'surprise':
            expression = 'shocked'
        elif dom_emot == 'disgust' :
            expression = 'annoyed'
        elif dom_emot == 'angry' :
            expression = 'upset' 

        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)                  
        cv2.putText(frame,
                    expression,
                    (50, 50),
                    font, 3,
                    (0, 0, 255),
                    2,
                    cv2.LINE_4)

    # logic for counting which emotion occured how many times
        final_emotion = result['dominant_emotion']
        if final_emotion == emotions[0]:
            smile_count = smile_count+1
        elif final_emotion == emotions[1]:
            worried_count = worried_count+1
        elif final_emotion == emotions[2]:
            pale_count = pale_count+1
        elif final_emotion == emotions[3]:
            anxious_count = anxious_count+1
        elif final_emotion == emotions[4]:
            surprise_count = surprise_count+1
        elif final_emotion == emotions[5]:
            other_count = other_count+1
        elif final_emotion == emotions[6]:
            angry_count = angry_count+1         

        cv2.imshow('video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):    #quiting the video frame
            break
    else :
        break     #autoclosing video after ending    
 
cap.release()
cv2.destroyAllWindows()

print("\nDetailed description about your expression :- ")
# setting threshold to define which emotion is occuring a lot and suggesting views on it
#thresholdcounting for vdo
smilenormal_threshold = frame_cnt/2
worriedanxioussurprise_threshold = frame_cnt/8
angry_threshold = frame_cnt/8
other_threshold = frame_cnt/7

if smile_count > smilenormal_threshold or pale_count > smilenormal_threshold :
    if smile_count > smilenormal_threshold:
        print("\nDetection outcome : smiled for too long.\n")
        print("Suggestion          : Having a little smile is always good while you speak but too much of smiling can affect the performance.\nWhy not try using some normal expression in between which can be helpful \n in gaining attention of public\n")
    if pale_count > smilenormal_threshold:
        print("\nDetection outcome : you looked too dull and expression less.\n")
        print("Suggestion          : Why not have some expression so get the attention of public and make this a little more intresting .\n Being more facially expressive will tent to make more impact on your audience \n")
if other_count > other_threshold:
    print("\nDetection outcome : You make some unusual\harsh face.\n")
    print("Suggestion          : Making such face is no good sign while speaking in front of audience. \n May lead to some hurtful meaning \n Try using some gentle expression !\n")
if angry_count > angry_threshold:
    print("\nDetection outcome : you expression showed angry multiple times.\n")
    print("Suggestion          : Take deep breathing ! Making an angry face while speking may lead to loosing audience attention.\n Try concentrating on good things while you speak in front of audience\n")
if anxious_count > worriedanxioussurprise_threshold or surprise_count > worriedanxioussurprise_threshold or worried_count > worriedanxioussurprise_threshold :
    if surprise_count > worriedanxioussurprise_threshold :
        print("\nDetection outcome : you looked surprised too many times.\n")
        print("Suggestion          : It could be a good expression to show you got surprised .\n But you made surprised face too many times try having some gentel expressions or\n avoid making this expression too many times \n")
    if worried_count > worriedanxioussurprise_threshold:
        print("\nDetection outcome : you looked nervous\n")
        print("Suggestion : Why be nervous ! Do some deep breathing to get relaxed .\n Focus on your material, not on your audience.\n Don't fear a moment of silence also you can have a\n little bit of smile on face to look more presentable and confident\n")
    if anxious_count > worriedanxioussurprise_threshold :
        print("\nDetection outcome : You looked anxious most of the time .\n")
        print("Suggestion          : You can improve your expressions ! To become more confident Practice, and then practice some more.\n While you’re speaking, make eye contact. \n")
else:
    print("\n Expression Outcome :  Your expressions were on point !\n Keep it up !!\n You are now ready for interacting with your audience\n All the best")

