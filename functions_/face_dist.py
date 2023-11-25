import dlib    #загрузка обученных моделей
from skimage import io     #считываеться изображение
from scipy.spatial import distance  #проверка на едентичность людей

def checkFace(img_path,img_path2):
    #загрузка скаченных моделей
    sp=dlib.shape_predictor("predictors_\shape_predictor_68_face_landmarks.dat") 
    facerec=dlib.face_recognition_model_v1('predictors_\dlib_face_recognition_resnet_model_v1.dat')

    img=io.imread(img_path)
    detector=dlib.get_frontal_face_detector()
    dets=detector(img,1)

    for k,d in enumerate(dets):
        shape=sp(img,d) # находит лицо человека

    face_descriptor1 = facerec.compute_face_descriptor(img, shape) # 128 значений, "контрольные точки" лица

    img = io.imread(img_path2)
    dets_webcam = detector(img, 1)

    for k, d in enumerate(dets_webcam):
        shape = sp(img, d)
    face_descriptor2=facerec.compute_face_descriptor(img,shape)

    #результат от 0 (100% один и тот же человек) до 1 (100% разные люди)
    result = distance.euclidean(face_descriptor1, face_descriptor2)

    if result<0.6:
        return True
    return False

#print(CheckFace("img/1g.jpg", "img/1gp.jpg"))